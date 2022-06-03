import os
from unittest import TestCase
from json import loads, dumps
from jsonpath_ng import parse


class TestClusterLogging(TestCase):
    def setUp(self):
        fp = open(os.getcwd() + "/test/data/test_aws_cluster_logging_resources.json", "r")
        content = fp.read()
        fp.close()
        self.resources = loads(content)

    def test_clusterlogging(self):
        """
        Tests logging is not enabled 
        """
        test = [match.value for match in parse('logging..enabled').find(self.resources)]
        flag = len(set(test)) == 1 and set(test).pop() in [True, 'true']
        self.assertEqual(True, flag, msg="Logging is not enabled")
