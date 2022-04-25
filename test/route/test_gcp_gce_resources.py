import os
from unittest import TestCase
from json import loads, dumps
from jsonpath_ng import parse


class TestInstances(TestCase):
    def setUp(self):
        fp = open(os.getcwd() + "/test/data/test_gcp_gce_resources.json", "r")
        content = fp.read()
        fp.close()
        self.resources = loads(content)

    def test_deletion_protection(self):
        """
        Tests either deletion protection is enabled or not
        """
        test = [match.value for match in parse('instance[*].self.source_data.deletionProtection').find(self.resources) if match.value in [False, 'false']]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="There are few instances with deletion protection disabled.")

    def test_default_service_account(self):
        """
        Tests compute instances is being used default service account or not
        """
        test = [match.value for match in parse('instance[*].self.source_data.serviceAccounts[*].email').find(self.resources) if  'compute@developer.gserviceaccount.com' in match.value]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="There are few instances with default service account being used.")
    
    def test_block_project_wise_ssh(self):
        """
        Tests either vm has project wise ssh disabled or not
        """
        test = [match.value for match in parse('instance[*].self.source_data.metadata.items[*]').find(self.resources) if match.value.get('key', '') == 'block-project-ssh-keys' and  match.value.get('value', '') in ['false', False]]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="There are few instances without disabled project wise ssh.")
    
    def test_shielded_vm(self):
        """
        Tests either vm has shielded vm enabled or not
        """
        test = [match.value for match in parse('instance[*].self.source_data').find(self.resources) if 'shieldedInstanceConfig' not in match.value or match.value.get('shieldedInstanceConfig', '').get('enableSecureBoot', '') in [False, 'false']]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="There are few instances without shielded vm enabled.")
    
    def test_vm_restart_policy(self):
        """
        Tests either vm has automatic restart enabled or not
        """
        test = [match.value for match in parse('instance[*].self.source_data.scheduling.automaticRestart').find(self.resources) if match.value in ['false', False]]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="There are few instances with automatic restart disabled.")
    
    def test_serial_port(self):
        """
        Tests either vm has serial port disabled or not
        """
        test = [match.value for match in parse('instance[*].self.source_data.metadata.items[*]').find(self.resources) if match.value.get('key', '') == 'serial-port-enable' and  match.value.get('value', '') in ['false', False]]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="There are few instances with serial port enabled.")
    