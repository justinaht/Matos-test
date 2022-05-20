import os
from unittest import TestCase
from json import loads, dumps
from jsonpath_ng import parse
import datetime

class TestServiceAccount(TestCase):
    def setUp(self):
        fp = open(os.getcwd() + "/test/data/test_gcp_snapshot_resources.json", "r")
        content = fp.read()
        fp.close()
        self.resources = loads(content)

    def test_check_disk_without_snapshot(self):
        """
        Check either all disks has snapshot available or not
        """
        fp = open(os.getcwd() + "/test/data/test_gcp_disk_resources.json", "r")
        content = fp.read()
        fp.close()
        self.disks = loads(content)
        snapshots = [match.value for match in
                parse('snapshot[*].self.source_data.resource.data.sourceDisk').find(self.resources)]
        test = [match.value for match in
                parse('disk[*].self.source_data.resource.data[*].selfLink').find(self.disks) if
                match.value not in snapshots]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="There are few disks without snapshots.")
    

    def test_check_old_snapshots(self):
        """
        Check either disk has older snapshot available or not
        """
        days = 3
        test = [match.value for match in
                parse('snapshot[*].self.source_data.resource.data.creationTimestamp').find(self.resources) if datetime.datetime.strptime(match.value[:-10], "%Y-%m-%dT%H:%M:%S")  + datetime.timedelta(days=days) < datetime.datetime.strptime(datetime.datetime.now().isoformat()[:-7], "%Y-%m-%dT%H:%M:%S")]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="There are few snatpshots with more then {} days old.".format(days))
    
    def test_label_attachement(self):
        """
        Check either snapshot has label attached or not
        """
        test = [match.value for match in
                parse('snapshot[*].self.source_data.resource.data').find(self.resources)  if not match.value.get('labels') or len(match.value.get('labels')) < 1]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="There are few snatpshots without label attached")
    
    