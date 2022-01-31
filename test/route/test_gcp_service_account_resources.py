import os
from unittest import TestCase
from json import loads, dumps
from jsonpath_ng import parse


class TestServiceAccount(TestCase):
    def setUp(self):
        fp = open(os.getcwd() + "/test/data/test_gcp_service_account_resources.json", "r")
        content = fp.read()
        fp.close()
        self.resources = loads(content)

    def test_check_service_account_with_project_wise_roles(self):
        """
        Check service account has project wise roles assigned or not
        """
        test = [match.value for match in parse('serviceAccount[*].self.iam_policy.bindings[*].role').find(self.resources) if  match.value in ['roles/editor', 'roles/owner']]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="There are few service accounts having administrative permission assinged.")

    def test_check_service_account_keys(self):
        """
        Check service account has customer created service account keys or not
        """
        test = [match.value for match in parse('serviceAccount[*].serviceAccountKey[*].self.keyType').find(self.resources) if  match.value == 'USER_MANAGED']
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="There are few service accounts having customer managed service account keys created.")


    def test_check_service_account_has_service_account_admin_binding(self):
        """
        Check service account has service account admin role binding
        """
        test = [match.value for match in parse('serviceAccount[*].self.iam_policy.bindings[*].role').find(self.resources) if  match.value == 'roles/iam.serviceAccountAdmin']
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="There are few service accounts having service account admin role binding to it.")










