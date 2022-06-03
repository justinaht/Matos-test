import os
from unittest import TestCase
from json import loads, dumps
from jsonpath_ng import parse


class TestCluster(TestCase):
    def setUp(self):
        fp = open(os.getcwd() + "/test/data/test_gcp_resources.json", "r")
        content = fp.read()
        fp.close()
        self.resources = loads(content)

    def test_k8dashboard(self):
        """
        Tests the kubernetes dashboard is disabled.
        """
        test = [match.value for match in parse('cluster[*].self..kubernetesDashboard.disabled').find(self.resources)]
        flag = len(set(test)) == 1 and set(test).pop() in [True, 'true']
        self.assertEqual(True, flag, msg="Kubernetes dashboard is enabled.")

    def test_k8networkpolicy(self):
        """
        Tests the kubernetes network policy config is enabled.
        """
        test = [match.value for match in parse('cluster[*].self..networkPolicyConfig.disabled').find(self.resources)]
        flag = len(set(test)) == 1 and set(test).pop() in [False, 'false']
        self.assertEqual(True, flag, msg="Cluster Network Policy is disabled.")

    def test_nodelegacyendpoints(self):
        """
        Tests the Node legacy endpoint is disabled.
        """
        test = [match.value for match in
                parse('cluster[*]..nodeConfig[*].metadata.disable-legacy-endpoints').find(self.resources)]
        flag = len(set(test)) == 1 and set(test).pop() in [True, 'true']
        self.assertEqual(True, flag, msg="Legacy endpoint is enabled")

    def test_defaultserviceaccount(self):
        """
        Tests default service account is not used
        """
        test = [match.value for match in parse('cluster[*].self..nodeConfig.serviceAccount').find(self.resources)]
        flag = len(set(test)) == 1 and set(test).pop() == 'default'
        self.assertEqual(True, flag, msg="Default service account is not used.")

    def test_loggingcomponents(self):
        """
        Tests logging is enabled for all log types - "SYSTEM_COMPONENTS", "WORKLOADS"
        """
        test = [match.value for match in parse('cluster[*]..loggingConfig..enableComponents').find(self.resources)]
        flag = len(test) >= 1 and len(set(test.pop())) >= 1
        self.assertEqual(True, flag, msg="Logging is not enabled for all log types")

    def test_monitoringcomponents(self):
        """
        Tests monitoring is enabled for all types - "SYSTEM_COMPONENTS", "WORKLOADS"
        """
        test = [match.value for match in parse('cluster[*]..monitoringConfig..enableComponents').find(self.resources)]
        flag = len(test) >= 1 and len(set(test.pop())) >= 1
        self.assertEqual(True, flag, msg="Monitoring is not enabled for all log types")

    def test_masterauthorizednetwork(self):
        """
        Tests master authorized network and network policy is enabled
        """
        test = [match.value for match in parse('cluster[*]..masterAuthorizedNetworkConfig').find(self.resources)]
        masterAuthorizedNetworkConfig = len(test) == 1 and test.pop()
        flag = isinstance(masterAuthorizedNetworkConfig, dict) and len(masterAuthorizedNetworkConfig.keys()) != 0
        self.assertEqual(True, flag, msg="master authorized network config is not enabled")

    def test_enablepodsecuritypolicy(self):
        """
        Tests Pod security policy is enabled or not
        """
        test = [match.value for match in parse('cluster[*]..pod..EnablePodSecurityPolicy').find(self.resources)]
        enabledSecurityPolicyPods = [each for each in test if each in ['true', True]]
        flag = len(enabledSecurityPolicyPods) > 0
        self.assertEqual(True, flag, msg="Pod Security Policy is not enabled.")

    def test_nodeusedcontaineroptimizedos(self):
        """
        Tests node used Container-Optimized OS or not
        """
        test = [match.value for match in parse('cluster[*]..node..status.nodeInfo.osImage').find(self.resources)]
        containerOptimizedOs = [each for each in test if 'Container-Optimized OS' in each]
        flag = len(containerOptimizedOs) > 0
        self.assertEqual(True, flag, msg="node not used Container-Optimized OS")

    def test_nodeautorepairupgrade(self):
        """
        Tests auto repair / auto upgrade is enabled
        """
        autoRepairEnable = [match.value for match in
                            parse('cluster[*].self..management.autoRepair').find(self.resources) if
                            match.value in [True, 'true']]
        autoUpgradeEnable = [match.value for match in
                             parse('cluster[*].self..management.autoUpgrade').find(self.resources) if
                             match.value in [True, 'true']]
        flag = len(autoRepairEnable) > 0 and len(autoUpgradeEnable) > 0
        self.assertEqual(True, flag, msg="auto repair or auto upgrade or both of them is not enabled.")

    def test_shieldnodes(self):
        """
        Test shield nodes is enable
        """
        test = [match.value for match in parse('cluster[*].self..shieldedNodes.enabled').find(self.resources) if
                match.value in [True, 'true']]
        flag = len(test) > 0
        self.assertEqual(True, flag, msg="shielded nodes is disabled.")
