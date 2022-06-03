import os
from unittest import TestCase
from json import loads, dumps
from jsonpath_ng import parse
import datetime

class TestServiceAccount(TestCase):
    def setUp(self):
        fp = open(os.getcwd() + "/test/data/test_gcp_service_account_resources.json", "r")
        content = fp.read()
        fp.close()
        self.resources = loads(content)

    def test_check_service_account_keys(self):
        """
        Check service account has customer created service account keys or not
        """
        test = [match.value for match in
                parse('serviceAccount[*].serviceAccountKey[*].self.keyType').find(self.resources) if
                match.value == 'USER_MANAGED']
        flag = len(test) > 0
        self.assertEqual(False, flag,
                         msg="There are few service accounts having customer managed service account keys created.")

    def test_check_service_account_has_service_account_admin_binding(self):
        """
        Check service account has service account admin role binding
        """
        test = [match.value for match in
                parse('serviceAccount[*].self.iam_policy.bindings[*].role').find(self.resources) if
                match.value == 'roles/iam.serviceAccountAdmin']
        flag = len(test) > 0
        self.assertEqual(False, flag,
                         msg="There are few service accounts having service account admin role binding to it.")

    def test_check_service_account_key_rotation(self):
        """
        Check service account keys hasn't rotate since last 90 days
        """
        days = 90
        test = [match.value for match in
                parse('serviceAccount[*].serviceAccountKey[*].self').find(self.resources) if
                match.value.get('keyType') == 'USER_MANAGED' and datetime.datetime.strptime(match.value.get('validAfterTime', ''), "%Y-%m-%dT%H:%M:%SZ")  + datetime.timedelta(days=days) < datetime.datetime.strptime(datetime.datetime.now().isoformat()[:-7], "%Y-%m-%dT%H:%M:%S")]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="There are few service accounts keys pending for rotation.")
