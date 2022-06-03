import os
from unittest import TestCase
from json import loads, dumps
from jsonpath_ng import parse


class TestCloudSql(TestCase):
    def setUp(self):
        fp = open(os.getcwd() + "/test/data/test_aws_policy_resources.json", "r")
        content = fp.read()
        fp.close()
        self.resources = loads(content)

