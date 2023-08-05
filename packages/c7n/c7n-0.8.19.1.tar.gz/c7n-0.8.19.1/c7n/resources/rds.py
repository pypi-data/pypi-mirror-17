# Copyright 2016 Capital One Services, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
RDS Resource Manager
====================

Example Policies
----------------

Find rds instances that are publicly available

.. code-block:: yaml

   policies:
      - name: rds-public
        resource: rds
        filters:
         - PubliclyAccessible: true

Find rds instances that are not encrypted

.. code-block:: yaml

   policies:
      - name: rds-non-encrypted
        resource: rds
        filters:
         - type: value
           key: StorageEncrypted
           value: true
           op: ne

"""
import functools
import logging
import re

from botocore.exceptions import ClientError
from concurrent.futures import as_completed

from c7n.actions import ActionRegistry, BaseAction, AutoTagUser
from c7n.filters import FilterRegistry, Filter, AgeFilter, OPERATORS, ValueFilter
from c7n.manager import resources
from c7n.query import QueryResourceManager
from c7n import tags
from c7n.utils import (
    local_session, type_schema, get_account_id,
    get_retry, chunks, generate_arn, snapshot_identifier)
from c7n.resources.kms import ResourceKmsKeyAlias

from skew.resources.aws import rds

log = logging.getLogger('custodian.rds')

filters = FilterRegistry('rds.filters')
actions = ActionRegistry('rds.actions')

filters.register('tag-count', tags.TagCountFilter)
filters.register('marked-for-op', tags.TagActionFilter)
actions.register('auto-tag-user', AutoTagUser)


@resources.register('rds')
class RDS(QueryResourceManager):
    """Resource manager for RDS DB instances.
    """

    class resource_type(rds.DBInstance.Meta):
        filter_name = 'DBInstanceIdentifier'

    filter_registry = filters
    action_registry = actions
    _generate_arn = _account_id = None
    retry = staticmethod(get_retry(('Throttled',)))

    def __init__(self, data, options):
        super(RDS, self).__init__(data, options)

    @property
    def account_id(self):
        if self._account_id is None:
            session = local_session(self.session_factory)
            self._account_id = get_account_id(session)
        return self._account_id

    @property
    def generate_arn(self):
        if self._generate_arn is None:
            self._generate_arn = functools.partial(
                generate_arn, 'rds', region=self.config.region,
                account_id=self.account_id, resource_type='db', separator=':')
        return self._generate_arn

    def augment(self, resources):
        filter(None, _rds_tags(
            self.get_model(),
            resources, self.session_factory, self.executor_factory,
            self.generate_arn, self.retry))
        return resources


def _rds_tags(
        model, dbs, session_factory, executor_factory, generate_arn, retry):
    """Augment rds instances with their respective tags."""

    def process_tags(db):
        client = local_session(session_factory).client('rds')
        arn = generate_arn(db[model.id])
        tag_list = None
        try:
            tag_list = retry(client.list_tags_for_resource, ResourceName=arn)['TagList']
        except ClientError as e:
            if e.response['Error']['Code'] not in ['DBInstanceNotFound']:
                log.warning("Exception getting rds tags  \n %s" % (e))
            return None
        db['Tags'] = tag_list or []
        return db

    # Rds maintains a low api call limit, so this can take some time :-(
    with executor_factory(max_workers=1) as w:
        return list(w.map(process_tags, dbs))

def _db_instance_eligible_for_backup(resource):
    db_instance_id = resource['DBInstanceIdentifier']

    # Database instance is not in available state
    if resource.get('DBInstanceStatus', '') != 'available':
        log.debug("DB instance %s is not in available state" %
            (db_instance_id))
        return False
    # The specified DB Instance is a member of a cluster and its backup retention should not be modified directly.
    #   Instead, modify the backup retention of the cluster using the ModifyDbCluster API
    if resource.get('DBClusterIdentifier', ''):
        log.debug("DB instance %s is a cluster member" %
            (db_instance_id))
        return False
    # DB Backups not supported on a read replica for engine postgres
    if (resource.get('ReadReplicaSourceDBInstanceIdentifier', '') and
            resource.get('Engine', '') == 'postgres'):
        log.debug("DB instance %s is a postgres read-replica" %
            (db_instance_id))
        return False
    # DB Backups not supported on a read replica running a mysql version before 5.6.
    if (resource.get('ReadReplicaSourceDBInstanceIdentifier', '') and
            resource.get('Engine', '') == 'mysql'):
        engine_version = resource.get('EngineVersion', '')
        # Assume "<major>.<minor>.<whatever>"
        match = re.match(r'(?P<major>\d+)\.(?P<minor>\d+)\..*', engine_version)
        if (match and int(match.group('major')) < 5 or
            (int(match.group('major')) == 5 and int(match.group('minor')) < 6)):
            log.debug("DB instance %s is a version %s mysql read-replica" %
                (db_instance_id, engine_version))
            return False
    return True


@filters.register('default-vpc')
class DefaultVpc(Filter):
    """ Matches if an rds database is in the default vpc
    """

    schema = type_schema('default-vpc')

    vpcs = None
    default_vpc = None

    def __call__(self, rdb):
        vpc_id = rdb['DBSubnetGroup']['VpcId']
        if self.vpcs is None:
            self.vpcs = set((vpc_id,))
            query_vpc = vpc_id
        else:
            query_vpc = vpc_id not in self.vpcs and vpc_id or None

        if query_vpc:
            client = local_session(self.manager.session_factory).client('ec2')
            self.log.debug("querying vpc %s" % vpc_id)
            vpcs = [v['VpcId'] for v
                    in client.describe_vpcs(VpcIds=[vpc_id])['Vpcs']
                    if v['IsDefault']]
            if not vpcs:
                return []
            self.default_vpc = vpcs.pop()
        return vpc_id == self.default_vpc and True or False


@filters.register('kms-alias')
class KmsKeyAlias(ResourceKmsKeyAlias):

    def process(self, resources, event=None):
        return self.get_matching_aliases(resources)


@actions.register('mark-for-op')
class TagDelayedAction(tags.TagDelayedAction):

    schema = type_schema(
        'mark-for-op', rinherit=tags.TagDelayedAction.schema,
        ops={'enum': ['delete', 'snapshot']})

    batch_size = 5

    def process(self, resources):
        session = local_session(self.manager.session_factory)
        return super(TagDelayedAction, self).process(resources)

    def process_resource_set(self, resources, tags):
        client = local_session(self.manager.session_factory).client('rds')
        for r in resources:
            arn = self.manager.generate_arn(r['DBInstanceIdentifier'])
            client.add_tags_to_resource(ResourceName=arn, Tags=tags)


@actions.register('auto-patch')
class AutoPatch(BaseAction):

    schema = type_schema(
        'auto-patch',
        minor={'type': 'boolean'}, window={'type': 'string'})

    def process(self, resources):
        client = local_session(
            self.manager.session_factory).client('rds')

        params = {'AutoMinorVersionUpgrade': self.data.get('minor', True)}
        if self.data.get('window'):
            params['PreferredMaintenanceWindow'] = self.data['minor']

        for r in resources:
            client.modify_db_instance(
                DBInstanceIdentifier=r['DBInstanceIdentifier'],
                **params)


@actions.register('tag')
@actions.register('mark')
class Tag(tags.Tag):

    concurrency = 2
    batch_size = 5

    def process_resource_set(self, resources, tags):
        client = local_session(
            self.manager.session_factory).client('rds')
        for r in resources:
            arn = self.manager.generate_arn(r['DBInstanceIdentifier'])
            client.add_tags_to_resource(ResourceName=arn, Tags=tags)


@actions.register('remove-tag')
@actions.register('unmark')
class RemoveTag(tags.RemoveTag):

    concurrency = 2
    batch_size = 5

    def process_resource_set(self, resources, tag_keys):
        client = local_session(
            self.manager.session_factory).client('rds')
        for r in resources:
            arn = self.manager.generate_arn(r['DBInstanceIdentifier'])
            client.remove_tags_from_resource(
                ResourceName=arn, TagKeys=tag_keys)


@actions.register('tag-trim')
class TagTrim(tags.TagTrim):

    def process_tag_removal(self, resource, candidates):
        client = local_session(
            self.manager.session_factory).client('rds')
        arn = self.manager.generate_arn(resource['DBInstanceIdentifier'])
        client.remove_tags_from_resource(ResourceName=arn, TagKeys=candidates)


@actions.register('delete')
class Delete(BaseAction):

    schema = {
        'type': 'object',
        'properties': {
            'type': {'enum': ['delete'],
                     'skip-snapshot': {'type': 'boolean'}}
            }
        }

    def process(self, resources):
        self.skip = self.data.get('skip-snapshot', False)

        # Concurrency feels like over kill here.
        client = local_session(self.manager.session_factory).client('rds')
        for rdb in resources:
            params = dict(
                DBInstanceIdentifier=rdb['DBInstanceIdentifier'])
            if self.skip:
                params['SkipFinalSnapshot'] = True
            else:
                params['FinalDBSnapshotIdentifier'] = snapshot_identifier(
                    'Final', rdb['DBInstanceIdentifier'])
            try:
                client.delete_db_instance(**params)
            except ClientError as e:
                if e.response['Error']['Code'] == "InvalidDBInstanceState":
                    continue
                raise

            self.log.info("Deleted rds: %s" % rdb['DBInstanceIdentifier'])


@actions.register('snapshot')
class Snapshot(BaseAction):

    schema = {'properties': {
        'type': {
            'enum': ['snapshot']}}}

    def process(self, resources):
        with self.executor_factory(max_workers=3) as w:
            futures = []
            for resource in resources:
                futures.append(w.submit(
                    self.process_rds_snapshot,
                    resource))
                for f in as_completed(futures):
                    if f.exception():
                        self.log.error(
                            "Exception creating rds snapshot  \n %s" % (
                                f.exception()))
        return resources

    def process_rds_snapshot(self, resource):
        if not _db_instance_eligible_for_backup(resource):
            return

        c = local_session(self.manager.session_factory).client('rds')
        c.create_db_snapshot(
            DBSnapshotIdentifier=snapshot_identifier(
                'Backup',
                resource['DBInstanceIdentifier']),
            DBInstanceIdentifier=resource['DBInstanceIdentifier'])


@actions.register('retention')
class RetentionWindow(BaseAction):

    date_attribute = "BackupRetentionPeriod"
    schema = type_schema(
        'retention',
        **{'days': {'type': 'number'}, 'copy-tags': {'type': 'boolean'}})

    def process(self, resources):
        with self.executor_factory(max_workers=3) as w:
            futures = []
            for resource in resources:
                futures.append(w.submit(
                    self.process_snapshot_retention,
                    resource))
                for f in as_completed(futures):
                    if f.exception():
                        self.log.error(
                            "Exception setting rds retention  \n %s" % (
                                f.exception()))

    def process_snapshot_retention(self, resource):
        current_retention = int(resource.get('BackupRetentionPeriod', 0))
        current_copy_tags = resource['CopyTagsToSnapshot']
        new_retention = self.data['days']
        new_copy_tags = self.data.get('copy-tags', True)

        if ((current_retention < new_retention or
                current_copy_tags != new_copy_tags) and
                _db_instance_eligible_for_backup(resource)):
            self.set_retention_window(
                resource,
                max(current_retention, new_retention),
                new_copy_tags)
            return resource

    def set_retention_window(self, resource, retention, copy_tags):
        c = local_session(self.manager.session_factory).client('rds')
        c.modify_db_instance(
            DBInstanceIdentifier=resource['DBInstanceIdentifier'],
            BackupRetentionPeriod=retention,
            CopyTagsToSnapshot=copy_tags)


@resources.register('rds-snapshot')
class RDSSnapshot(QueryResourceManager):
    """Resource manager for RDS DB snapshots.
    """

    class Meta(object):

        service = 'rds'
        type = 'rds-snapshot'
        enum_spec = ('describe_db_snapshots', 'DBSnapshots', None)
        name = id = 'DBSnapshotIdentifier'
        filter_name = None
        filter_type = None
        dimension = None
        date = 'SnapshotCreateTime'

    resource_type = Meta

    filter_registry = FilterRegistry('rds-snapshot.filters')
    action_registry = ActionRegistry('rds-snapshot.actions')


@RDSSnapshot.filter_registry.register('age')
class RDSSnapshotAge(AgeFilter):

    schema = type_schema(
        'age', days={'type': 'number'},
        op={'type': 'string', 'enum': OPERATORS.keys()})

    date_attribute = 'SnapshotCreateTime'


@RDSSnapshot.action_registry.register('delete')
class RDSSnapshotDelete(BaseAction):

    def process(self, snapshots):
        log.info("Deleting %d rds snapshots", len(snapshots))
        with self.executor_factory(max_workers=3) as w:
            futures = []
            for snapshot_set in chunks(reversed(snapshots), size=50):
                futures.append(
                    w.submit(self.process_snapshot_set, snapshot_set))
                for f in as_completed(futures):
                    if f.exception():
                        self.log.error(
                            "Exception deleting snapshot set \n %s" % (
                                f.exception()))
        return snapshots

    def process_snapshot_set(self, snapshots_set):
        c = local_session(self.manager.session_factory).client('rds')
        for s in snapshots_set:
            try:
                c.delete_db_snapshot(
                    DBSnapshotIdentifier=s['DBSnapshotIdentifier'])
            except ClientError as e:
                raise
