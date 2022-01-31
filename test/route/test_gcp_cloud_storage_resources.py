import os
from unittest import TestCase
from json import loads, dumps
from jsonpath_ng import parse


class TestCloudStorage(TestCase):
    def setUp(self):
        fp = open(os.getcwd() + "/test/data/test_gcp_cloud_storage_resources.json", "r")
        content = fp.read()
        fp.close()
        self.resources = loads(content)
    
    def test_public_access(self):
        """
        Check bucket is publicly accessible or not
        """
        test = [match.value for match in parse('storage[*].self.iam_policy.bindings[*].members[*]').find(self.resources) if match.value == 'allUsers']
        flag = len(test) > 0
        self.assertEqual(True, flag, msg="There are few buckets which are publicly accessible.")

    
    def test_check_retention_policy(self):
        """
        Check retention policy has been applied or not
        """
        test = [match.value for match in parse('storage[*].self.resource.retentionPolicy').find(self.resources) if len(match.value) < 1]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="There are few buckets without retention policy applied.")

    def test_check_lifecycle_policy(self):
        """
        Check lifecycle policy has been applied or not
        """
        test = [match.value for match in parse('storage[*].self.resource.lifecycle.rule').find(self.resources) if len(match.value) < 1]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="There are few buckets without lifecycle policy applied.")

    def test_check_cmek(self):
        """
        Check bucket encrypted with CMEK.
        """
        test = [match.value for match in parse('storage[*].self.resource.encryption').find(self.resources) if len(match.value) < 1]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="There are few buckets without encrypted with CMEK.")

    def test_check_uniform_bucket_access(self):
        """
        Check uniform bucket policy
        """
        test = [match.value for match in parse('storage[*].self.resource.iamConfiguration.uniformBucketLevelAccess.enabled').find(self.resources) if match.value in [False, 'false']]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="There are few buckets without uniform  bucket access policy.")
    
    def test_check_public_access_prevention_enabled(self):
        """
        Check either public access prevention option is enabled or not
        """
        test = [match.value for match in parse('storage[*].self.resource.iamConfiguration.publicAccessPrevention').find(self.resources) if match.value != "enforced"]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="There are few buckets without public access prevention enabled.")
    
    def test_check_all_bucket_has_label_applied(self):
        """
        Check either bucket has label applied or not
        """
        test = [match.value for match in parse('storage[*].self.resource.labels').find(self.resources) if len(match.value)< 1]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="There are few buckets without label applied.")
    






