import os
from unittest import TestCase
from json import loads, dumps
from jsonpath_ng import parse


class TestCloudSql(TestCase):
    def setUp(self):
        fp = open(os.getcwd() + "/test/data/test_gcp_cloud_sql_resources.json", "r")
        content = fp.read()
        fp.close()
        self.resources = loads(content)

    def test_check_instances_with_public_ip(self):
        """
        Check cloud sql server with public ip address
        """
        test = [match.value for match in parse('sql[*].self.source_data.ipAddresses[*]..type').find(self.resources) if
                match.value == 'PRIMARY']
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="There are few sql instances with public IP address.")

    def test_check_instances_with_open_to_all(self):
        """
        Check cloud sql server with open to all network
        """
        test = [match.value for match in
                parse('sql[*].self.source_data.settings.ipConfiguration.authorizedNetworks[*].value').find(
                    self.resources) if match.value == '0.0.0.0/0']
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="There are few sql instances with open to all network.")

    def test_check_instances_with_size_auto_increase(self):
        """
        Check cloud sql server with autoincrease size
        """
        test = [match.value for match in
                parse('sql[*].self.source_data.settings.storageAutoResize').find(self.resources) if
                match.value in [False, 'false']]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="There are few sql instances with auto increase size is disabled.")

    def test_check_instances_without_ssd(self):
        """
        Check cloud sql server without ssd
        """
        test = [match.value for match in parse('sql[*].self.source_data.settings.dataDiskType').find(self.resources) if
                match.value == 'PD_HDD']
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="There are few sql instances without Solid State Drive.")

    def test_check_instances_high_avaibility(self):
        """
        Check cloud sql server without high availbility configured.
        """
        test = [match.value for match in parse('sql[*].self.source_data.settings.availabilityType').find(self.resources)
                if match.value == 'ZONAL']
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="There are few sql instances without high availbility configured.")

    def test_check_instances_fail_over_replica(self):
        """
        Check cloud sql server without fail over replica configured.
        """
        test = [match.value for match in parse('sql[*].self.source_data').find(self.resources) if
                not match.value.get('failoverReplica', False)]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="There are few instances without failover replica configured.")

    def test_check_instances_without_ssl_connection(self):
        """
        Check cloud sql server without ssl connection configured
        """
        test = [match.value for match in
                parse('sql[*].self.source_data.settings.ipConfiguration.requireSsl').find(self.resources) if
                match.value in [False, 'false']]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="There are few sql instances without ssl connection configured.")

    def test_check_instances_without_backup_enabled(self):
        """
        Check cloud sql server without backup configured
        """
        test = [match.value for match in
                parse('sql[*].self.source_data.settings.backupConfiguration.enabled').find(self.resources) if
                match.value in [False, 'false']]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="There are few sql instances without backup configured.")

    def test_check_instances_without_cmek(self):
        """
        Check cloud sql server without customer managed encryption keys enabled
        """
        test = [match.value for match in parse('sql[*].self.source_data').find(self.resources) if
                not match.value.get('diskEncryptionStatus', False)]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="There are few sql instances without customer managed encryption key.")

    def test_check_instances_label(self):
        """
        Check cloud sql server without labeling
        """
        test = [match.value for match in parse('sql[*].self.source_data.settings').find(self.resources) if
                not match.value.get('userLabels', False)]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="There are few sql instances without labeling.")

        
    def test_binary_logging(self):
        """
        Check cloud sql server without binary logging enable
        """
        test = [match.value for match in parse('sql[*].self.source_data.settings.backupConfiguration').find(self.resources) if
                not match.value.get('binaryLogEnabled', False)]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="There are few sql instances without binary logging enable.")
