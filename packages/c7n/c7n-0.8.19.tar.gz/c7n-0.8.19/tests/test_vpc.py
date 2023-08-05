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
from common import BaseTest


class NetworkInterfaceTest(BaseTest):

    def test_interface_subnet(self):
        factory = self.replay_flight_data(
            'test_network_interface_filter')

        client = factory().client('ec2')
        vpc_id = client.create_vpc(CidrBlock="10.4.0.0/16")['Vpc']['VpcId']
        self.addCleanup(client.delete_vpc, VpcId=vpc_id)

        sub_id = client.create_subnet(
            VpcId=vpc_id, CidrBlock="10.4.8.0/24")[
                'Subnet']['SubnetId']
        self.addCleanup(client.delete_subnet, SubnetId=sub_id)

        sg_id = client.create_security_group(
            GroupName="web-tier",
            VpcId=vpc_id,
            Description="for apps")['GroupId']
        self.addCleanup(client.delete_security_group, GroupId=sg_id)

        qsg_id = client.create_security_group(
            GroupName="quarantine-group",
            VpcId=vpc_id,
            Description="for quarantine")['GroupId']
        self.addCleanup(client.delete_security_group, GroupId=qsg_id)

        net = client.create_network_interface(
            SubnetId=sub_id, Groups=[sg_id])['NetworkInterface']
        net_id = net['NetworkInterfaceId']
        self.addCleanup(
            client.delete_network_interface, NetworkInterfaceId=net_id)

        p = self.load_policy({
            'name': 'net-find',
            'resource': 'eni',
            'filters': [
                {'type': 'subnet',
                 'key': 'SubnetId',
                 'value': sub_id},
                {'type': 'group',
                 'key': 'Description',
                 'value': 'for apps'}
            ],
            'actions': [{
                'type': 'remove-groups',
                'groups': 'matched',
                'isolation-group': qsg_id}]
            }, session_factory=factory)
        resources = p.run()
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0]['NetworkInterfaceId'], net_id)
        self.assertEqual(resources[0]['MatchedSecurityGroups'], [sg_id])
        results = client.describe_network_interfaces(
            NetworkInterfaceIds=[net_id])['NetworkInterfaces']
        self.assertEqual([g['GroupId'] for g in results[0]['Groups']], [qsg_id])


class SecurityGroupTest(BaseTest):

    def test_unused(self):
        factory = self.replay_flight_data(
            'test_security_group_unused')
        p = self.load_policy({
            'name': 'sg-unused',
            'resource': 'security-group',
            'filters': ['unused'],
            }, session_factory=factory)
        resources = p.run()
        self.assertEqual(len(resources), 1)

    def test_only_ports(self):
        factory = self.replay_flight_data(
            'test_security_group_only_ports')
        client = factory().client('ec2')
        vpc_id = client.create_vpc(CidrBlock="10.4.0.0/16")['Vpc']['VpcId']
        self.addCleanup(client.delete_vpc, VpcId=vpc_id)
        sg_id = client.create_security_group(
            GroupName="web-tier",
            VpcId=vpc_id,
            Description="for apps")['GroupId']
        self.addCleanup(client.delete_security_group, GroupId=sg_id)
        client.authorize_security_group_ingress(
            GroupId=sg_id,
            IpProtocol='tcp',
            FromPort=60000,
            ToPort=62000,
            CidrIp='10.2.0.0/16')
        client.authorize_security_group_ingress(
            GroupId=sg_id,
            IpProtocol='tcp',
            FromPort=61000,
            ToPort=61000,
            CidrIp='10.2.0.0/16')
        p = self.load_policy({
            'name': 'sg-find',
            'resource': 'security-group',
            'filters': [
                {'type': 'ingress',
                 'OnlyPorts': [61000]},
                {'GroupName': 'web-tier'}]
            }, session_factory=factory)
        resources = p.run()
        self.assertEqual(len(resources), 1)
        self.assertEqual(
            resources[0]['MatchedIpPermissions'],
            [{u'FromPort': 60000,
              u'IpProtocol': u'tcp',
              u'IpRanges': [{u'CidrIp': u'10.2.0.0/16'}],
              u'PrefixListIds': [],
              u'ToPort': 62000,
              u'UserIdGroupPairs': []}])

    def test_port_within_range(self):
        factory = self.replay_flight_data(
            'test_security_group_port_in_range')
        client = factory().client('ec2')
        vpc_id = client.create_vpc(CidrBlock="10.4.0.0/16")['Vpc']['VpcId']
        self.addCleanup(client.delete_vpc, VpcId=vpc_id)
        sg_id = client.create_security_group(
            GroupName="web-tier",
            VpcId=vpc_id,
            Description="for apps")['GroupId']
        self.addCleanup(client.delete_security_group, GroupId=sg_id)
        client.authorize_security_group_ingress(
            GroupId=sg_id,
            IpProtocol='tcp',
            FromPort=60000,
            ToPort=62000,
            CidrIp='10.2.0.0/16')
        p = self.load_policy({
            'name': 'sg-find',
            'resource': 'security-group',
            'filters': [
                {'type': 'ingress',
                 'IpProtocol': 'tcp',
                 'FromPort': 60000},
                {'GroupName': 'web-tier'}]
            }, session_factory=factory)
        resources = p.run()
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0]['GroupName'], 'web-tier')
        self.assertEqual(
            resources[0]['MatchedIpPermissions'],
            [{u'FromPort': 60000,
              u'IpProtocol': u'tcp',
              u'IpRanges': [{u'CidrIp': u'10.2.0.0/16'}],
              u'PrefixListIds': [],
              u'ToPort': 62000,
              u'UserIdGroupPairs': []}])

    def test_ingress_remove(self):
        factory = self.replay_flight_data(
            'test_security_group_ingress_filter')
        client = factory().client('ec2')
        vpc_id = client.create_vpc(CidrBlock="10.4.0.0/16")['Vpc']['VpcId']
        sg_id = client.create_security_group(
            GroupName="web-tier",
            VpcId=vpc_id,
            Description="for apps")['GroupId']
        self.addCleanup(client.delete_vpc, VpcId=vpc_id)
        client.authorize_security_group_ingress(
            GroupId=sg_id,
            IpProtocol='tcp',
            FromPort=0,
            ToPort=62000,
            CidrIp='10.2.0.0/16')
        self.addCleanup(client.delete_security_group, GroupId=sg_id)
        p = self.load_policy({
            'name': 'sg-find',
            'resource': 'security-group',
            'filters': [
                {'VpcId': vpc_id},
                {'type': 'ingress',
                 'IpProtocol': 'tcp',
                 'FromPort': 0},
                {'GroupName': 'web-tier'}],
            'actions': [
                {'type': 'remove-permissions',
                 'ingress': 'matched'}]},
            session_factory=factory)
        resources = p.run()
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0]['GroupId'], sg_id)
        group_info = client.describe_security_groups(
            GroupIds=[sg_id])['SecurityGroups'][0]
        self.assertEqual(group_info.get('IpPermissions', []), [])

    def test_default_vpc(self):
        # preconditions, more than one vpc, each with at least one
        # security group
        factory = self.replay_flight_data(
            'test_security_group_default_vpc_filter')
        p = self.load_policy({
            'name': 'sg-test',
            'resource': 'security-group',
            'filters': [
                {'type': 'default-vpc'},
                {'GroupName': 'default'}]},
            session_factory=factory)
        resources = p.run()
        self.assertEqual(len(resources), 1)


class VpcTest(BaseTest):

    def test_subnets(self):
        factory = self.replay_flight_data(
            'test_vpc_subnets_filter')
        p = self.load_policy({
            'name': 'empty-vpc-test',
            'resource': 'vpc',
            'filters': [
                {'type': 'subnets',
                 'value': []}]},
            session_factory=factory)
        resources = p.run()
        self.assertEqual(len(resources), 1)
