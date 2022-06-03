import os
from unittest import TestCase
from json import loads, dumps
from jsonpath_ng import parse


class TestAWSEC2InstanceRole(TestCase):
    def setUp(self):
        fp = open(os.getcwd() + "/test/data/test_aws_resources.json", "r")
        content = fp.read()
        fp.close()
        self.resources = loads(content)

    def test_instance_profile_assigned_or_not(self):
        """
        Check if EC2 instance is assigned an instance profile or not.
        Note: To assign a role to the EC2 instance an instance profile is assigned.
        """
        test = [match.value for match in parse('instance[*].self[*].IamInstanceProfile').find(self.resources)]
        flag = len(test) == len(self.resources.get("instance"))
        self.assertEqual(True, flag, msg="Instance profile is not attached")

    def test_instance_profile_associated_with_role(self):
        """
        Check if instance profile is associated with a role
        """
        test = [match.value for match in parse('instance[*].self[*].IamInstanceProfile.Roles[0]').find(self.resources)]
        flag = len(test) == len(self.resources.get("instance"))
        self.assertEqual(True, flag, msg="Instance profile is not associated with a role")

    def test_trust_principal_is_ec2(self):
        """
        Check if assume role policy document associated with the instance role is having permission for the EC2 service.
        """
        criteria = 'instance[*].self[*].IamInstanceProfile.Roles[*].AssumeRolePolicyDocument.Statement[*].Principal.Service'
        test = [match.value for match in parse(criteria).find(self.resources)]
        flag = len(set(test)) == 1 and set(test).pop() in ['ec2.amazonaws.com']
        self.assertEqual(True, flag, msg="Principal in assume role policy document is not ec2 service")        
  
