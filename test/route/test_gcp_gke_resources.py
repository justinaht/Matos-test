import os
from unittest import TestCase
from json import loads, dumps
from jsonpath_ng import parse


class TestCluster(TestCase):
    def setUp(self):
        fp = open(os.getcwd() + "/test/data/test_gcp_gke_resources.json", "r")
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

    def test_k8network_policy(self):
        """
        Tests the kubernetes network policy config is enabled.
        """
        test = [match.value for match in parse('cluster[*].self..networkPolicyConfig.disabled').find(self.resources)]
        flag = len(set(test)) == 1 and set(test).pop() in [False, 'false']
        self.assertEqual(True, flag, msg="Cluster Network Policy is disabled.")

    def test_node_legacy_endpoints(self):
        """
        Tests the Node legacy endpoint is disabled.
        """
        test = [match.value for match in
                parse('cluster[*]..nodeConfig[*].metadata.disable-legacy-endpoints').find(self.resources)]
        flag = len(set(test)) == 1 and set(test).pop() in [True, 'true']
        self.assertEqual(True, flag, msg="Legacy endpoint is enabled")

    def test_default_serviceaccount(self):
        """
        Tests default service account is not used
        """
        test = [match.value for match in parse('cluster[*].self..nodeConfig.serviceAccount').find(self.resources)]
        flag = len(set(test)) == 1 and set(test).pop() == 'default'
        self.assertEqual(True, flag, msg="Default service account is not used.")

    def test_logging_components(self):
        """
        Tests logging is enabled for all log types - "SYSTEM_COMPONENTS", "WORKLOADS"
        """
        test = [match.value for match in parse('cluster[*]..loggingConfig..enableComponents').find(self.resources)]
        flag = len(test) >= 1 and len(set(test.pop())) >= 1
        self.assertEqual(True, flag, msg="Logging is not enabled for all log types")

    def test_monitoring_components(self):
        """
        Tests monitoring is enabled for all types - "SYSTEM_COMPONENTS", "WORKLOADS"
        """
        test = [match.value for match in parse('cluster[*]..monitoringConfig..enableComponents').find(self.resources)]
        flag = len(test) >= 1 and len(set(test.pop())) >= 1
        self.assertEqual(True, flag, msg="Monitoring is not enabled for all log types")

    def test_master_authorized_network(self):
        """
        Tests master authorized network and network policy is enabled
        """
        test = [match.value for match in parse('cluster[*]..masterAuthorizedNetworkConfig').find(self.resources)]
        master_authorized_network_config = len(test) == 1 and test.pop()
        flag = isinstance(master_authorized_network_config, dict) and len(master_authorized_network_config.keys()) != 0
        self.assertEqual(True, flag, msg="master authorized network config is not enabled")

    def test_enable_pod_security_policy(self):
        """
        Tests Pod security policy is enabled or not
        """
        test = [match.value for match in parse('cluster[*]..pod..EnablePodSecurityPolicy').find(self.resources)]
        enabled_security_policy_pods = [each for each in test if each in ['true', True]]
        flag = len(enabled_security_policy_pods) > 0
        self.assertEqual(True, flag, msg="Pod Security Policy is not enabled.")

    def test_node_used_container_optimized_os(self):
        """
        Tests node used Container-Optimized OS or not
        """
        test = [match.value for match in parse('cluster[*]..node..status.nodeInfo.osImage').find(self.resources)]
        container_optimized_os = [each for each in test if 'Container-Optimized OS' in each]
        flag = len(container_optimized_os) > 0
        self.assertEqual(True, flag, msg="node not used Container-Optimized OS")

    def test_node_auto_repair_upgrade(self):
        """
        Tests auto repair / auto upgrade is enabled
        """
        auto_repair_enable = [match.value for match in
                              parse('cluster[*].self..management.autoRepair').find(self.resources) if
                              match.value in [True, 'true']]
        auto_upgrade_enable = [match.value for match in
                               parse('cluster[*].self..management.autoUpgrade').find(self.resources) if
                               match.value in [True, 'true']]
        flag = len(auto_repair_enable) > 0 and len(auto_upgrade_enable) > 0
        self.assertEqual(True, flag, msg="auto repair or auto upgrade or both of them is not enabled.")

    def test_shield_nodes(self):
        """
        Test shield nodes is enable
        """
        test = [match.value for match in parse('cluster[*].self..shieldedNodes.enabled').find(self.resources) if
                match.value in [True, 'true']]
        flag = len(test) > 0
        self.assertEqual(True, flag, msg="shielded nodes is disabled.")

    def test_private_cluster(self):
        """
        Test private cluster is enable 
        """
        test = [match.value for match in parse('cluster[*].self..privateClusterConfig').find(self.resources)]
        flag = len(test) > 0
        self.assertEqual(True, flag, msg="Private cluster is not enabled.")

    def test_default_vpc(self):
        """
        Test default VPC is being used or not
        """
        test = [match.value for match in parse('cluster[*].self.source_data.network').find(self.resources)]

        default_vpc = [vpc for vpc in test if 'default' == vpc]
        flag = len(default_vpc) > 0
        self.assertEqual(False, flag, msg="Clusters is being used default VPC.")

    def test_regional_cluster(self):
        """
        Test either clusters are highly available or not
        """
        test = [match.value for match in parse('cluster[*].self.region').find(self.resources) if
                len(match.value.split('-')) > 2]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="The clusters are not highly available across the region.")

    def test_auto_scalling(self):
        """
        Check autoscalling is enable or not for node pools
        """
        test = [match.value for match in
                parse('cluster[*].self.source_data.nodePools..autoscaling.enabled').find(self.resources)]
        disabled_autoscaling = [autoscale for autoscale in test if autoscale in [False, 'false']]
        flag = len(disabled_autoscaling) > 0
        self.assertEqual(False, flag, msg="Autoscalling has not been enabled for Node pool.")

    def test_image_pull_policy(self):
        """
        Check image pull policy is IfNotPresent or not
        """
        test = [match.value for match in
                parse('cluster[*].pod[*].self.source_data.spec.containers[*].imagePullPolicy').find(self.resources)]
        image_pull_policies = [policy for policy in test if policy != "IfNotPresent"]
        flag = len(image_pull_policies) > 0
        self.assertEqual(False, flag, msg="Image pull policy has not configured as IFNotPresent.")

    def test_liveness_probe(self):
        """
        Check either liveness probe has been configured or not for container
        """
        test = [match.value for match in
                parse('cluster[*].pod[*].self.source_data.spec.containers[*]').find(self.resources) if
                not match.value.get("livenessProbe", False)]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="Container doesn't have liveness probe configured.")

    def test_readiness_probe(self):
        """
        Check either readinessProbe has been configured or not for container
        """
        test = [match.value for match in
                parse('cluster[*].pod[*].self.source_data.spec.containers[*]').find(self.resources) if
                not match.value.get("readinessProbe", False)]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="Container doesn't have readinessProbe configured.")

    def test_statefulset(self):
        """
        Check either statefulset workload is available or not
        """
        test = [match.value for match in
                parse('cluster[*].pod[*].self.source_data.metadata.ownerReferences[*].kind').find(self.resources) if
                match.value == "StatefulSet"]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="Stateful set workload is available.")

    def test_check_vpc_native_cluster(self):
        """
        Check cluster is using vpc native clusters
        """
        test = [match.value for match in parse('cluster[*].self.source_data.ipAllocationPolicy').find(self.resources) if
                match.value.get('useRoutes', False)]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="there are few gke clusters created without vpc native clusters.")

    def test_check_gke_meta_data_server(self):
        """
        Check cluster metadata server is enabled or not
        """
        test = [match.value for match in parse('cluster[*].self.source_data.nodeConfig').find(self.resources) if
                not match.value.get('workloadMetadataConfig', False)]
        other_meta_data_type = [match.value for match in
                                parse('cluster[*].self.source_data.nodeConfig.workloadMetadataConfig.mode').find(
                                    self.resources) if match.value not in ['GKE_METADATA']]
        flag = len(test) or len(other_meta_data_type) > 0
        self.assertEqual(False, flag, msg="There are few clusters without enabled metadata server.")

    def test_check_alpha_server(self):
        """
        Check cluster has alpha feature enabled or not
        """
        test = [match.value for match in parse('cluster[*].self.source_data.enableKubernetesAlpha').find(self.resources)
                if match.value in [True, 'true']]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="There are few clusters with alpha features enabled.")

    def test_check_intra_node_visibility(self):
        """
        Check cluster has intra node visibility
        """
        test = [match.value for match in
                parse('cluster[*].self.source_data.networkConfig.enableIntraNodeVisibility').find(self.resources) if
                match.value in [True, 'true']]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="There are few clusters with intra node visibility enabled.")

    def test_check_resources_get_labeled(self):
        """
        Check cluter labels availbility
        """
        test = [match.value for match in parse('cluster[*].pod[*].self.source_data.metadata').find(self.resources) if
                not match.value.get('labels', False)]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="few of the clusters resources doesn't have labeled applied.")
    
    def test_check_preemtiable_vm(self):
        """
        Check cluster has preemtiable vm used or not
        """
        test = [match.value for match in parse('cluster[*]..nodeConfig.preemptible').find(self.resources) if match.value in [True, 'true'] ]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="There are few clusters with preemtiable vm enabled.")
    
    def test_check_cluster_labels(self):
        """
        Check cluster has labels applied or not
        """
        test = [match.value for match in parse('cluster[*].self..resourceLabels').find(self.resources) if
                len(match.value) < 1]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="There are few clusters without labels.")
    