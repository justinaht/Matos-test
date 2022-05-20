from operator import truediv
import os
from unittest import TestCase
from json import loads, dumps
from jsonpath_ng import parse
import re  

class TestCluster(TestCase):
    def setUp(self):
        fp = open(os.getcwd() + "/test/data/test_aws_iam_resources.json", "r")
        content = fp.read()
        fp.close()
        self.resources = loads(content)

    def test_iam_policy_attached_to_user(self):
        """
        Ensure IAM policies are attached only to groups or roles
        """
        test = [match.value for match in parse('serviceAccount[*].self.UserName').find(self.resources) if re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', match.value) and match.value.get('PasswordEnable') in ['true', True]]
        flag = len(test)
        self.assertEqual(False, flag, msg="There are few users having policy attached directly.")
    
    def test_user_has_custom_policy_wildcard_permissions(self):
        """
        Check user has customer manage policy attached which support wildcard permission
        """
        test = [match.value for match in parse('serviceAccount[*].self.AttachedManagedPolicies[*]').find(self.resources) if 'Local' in match.value.get('Scope') and  [policy for policy in parse('Document.Statement[*]').find(match.value.get('PolicyVersion')) if 'Allow' in policy.value.get('Effect') and '*' in policy.value.get('Action') ]]
        flag = len(test)
        self.assertEqual(False, flag, msg="There are few policies with wildcard permissions assigned to the users")



# serviceAccount
