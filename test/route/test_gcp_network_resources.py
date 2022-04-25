import os
from unittest import TestCase
from json import loads, dumps
from jsonpath_ng import parse


class TestNetwork(TestCase):
    def setUp(self):
        fp = open(os.getcwd() + "/test/data/test_gcp_network_resources.json", "r")
        content = fp.read()
        fp.close()
        self.resources = loads(content)

    def test_exist_default_network(self):
        """
        Test if there is existed default network created or not
        """
        test = [match.value for match in parse('network[*].self.name').find(self.resources) if match.value == 'default']
        flag = len(test) == 1
        self.assertEqual(True, flag, msg="There is no existed default network")

    def test_default_network_auto_create_subnetwork(self):
        """
        Test default network can create automatically subnetworks
        """
        default_network = [network for network in self.resources['network'] if network['self']['name'] == 'default']
        test = [match.value for match in parse('defaultNetwork[*].self.source_data.autoCreateSubnetworks').find(
            {"defaultNetwork": default_network})]
        flag = len(test) > 0 and len([val for val in test if val in ['true', True]]) > 0
        self.assertEqual(True, flag, msg="Default network can not create automatically sub-networks")

    def test_non_default_network_auto_create_subnetwork(self):
        """
        Test non-default network can create automatically subnetworks
        """
        default_network = [network for network in self.resources['network'] if network['self']['name'] != 'default']
        test = [match.value for match in parse('defaultNetwork[*].self.source_data.autoCreateSubnetworks').find(
            {"defaultNetwork": default_network})]
        flag = len(test) > 0 and len([val for val in test if val in ['true', True]]) == 0
        self.assertEqual(True, flag, msg="Non default network can create automatically sub-networks")

    def test_all_subnetwork_private_purpose(self):
        """
        Test all subnetworks are private or not
        """
        test = [match.value for match in parse('network[*].subnetwork..purpose').find(self.resources)]
        flag = 0 < len(test) == len([val for val in test if val == 'PRIVATE'])
        self.assertEqual(True, flag, msg="There are some non-private subnetworks")

    def test_subnetwork_private_ip_google_access(self):
        """
        Test either subnetworks have private google access or not
        """
        test = [match.value for match in parse('network[*].subnetwork..privateIpGoogleAccess').find(self.resources) if
                match.value in ['false', False]]
        flag = 0 < len(test)
        self.assertEqual(False, flag, msg="Someof the subnetwork doens't have private google access.")

    def test_subnetwork_log(self):
        """
        Test subnetwork log is enabled or not
        """
        test = [match.value for match in parse('network[*].subnetwork..logConfig.enable').find(self.resources)]
        flag = len(test) > 0 and len([val for val in test if val in ['true', True]]) == 0
        self.assertEqual(False, flag, "all subnetworks are not enabled for log")
        flag = 0 < len(test) == len([val for val in test if val in ['true', True]])
        self.assertEqual(False, flag, msg="All subnetwors are enabled for log")

    def test_subnetwork_flow_log(self):
        """
        Test subnetwork flow log is enabled or not
        """
        test = [match.value for match in parse('network[*].subnetwork..enableFlowLogs').find(self.resources)]
        flag = len(test) > 0 and len([val for val in test if val in ['true', True]]) == 0
        self.assertEqual(False, flag, "all subnetworks are not enabled for flow log")
        flag = 0 < len(test) == len([val for val in test if val in ['true', True]])
        self.assertEqual(False, flag, msg="All subnetwors are enabled for flow log")

    def test_firewall_disabled(self):
        """
        Test firewall disabled or not
        """
        test = [match.value for match in parse('network[*].firewall..disabled').find(self.resources)]
        flag = len(test) > 0 and len([val for val in test if val in ['true', True]]) == 0
        self.assertEqual(True, flag, msg="Some firewalls is disabled")

    def test_firewall_log(self):
        """
        Test firewall log is disabled or not
        """
        test = [match.value for match in parse('network[*].firewall..logConfig.enable').find(self.resources)]
        flag = len(test) > 0 and len([val for val in test if val in ['true', True]]) == 0
        self.assertEqual(False, flag, "All firewall logs are disabled")
        flag = len(test) > 0 and len([val for val in test if val in ['false', False]]) == 0
        self.assertEqual(False, flag, "All firewall log are enabled")

    def test_check_rdp_open_access(self):
        """
        check RDP access from open netork
        """
        port = '3389'
        source_range = '0.0.0.0/0'
        test = [match.value for match in parse('network[*].firewall[*].self.source_data').find(self.resources) if
                port in [port.value for port in parse('allowed[*].ports[*]').find(match.value)] and source_range in [
                    source_range.value for source_range in parse('sourceRanges[*]').find(match.value)]]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="RDP access is opend for all.")

    def test_check_dns_open_access(self):
        """
        check DNS access from open netork
        """
        port = '35'
        source_range = '0.0.0.0/0'
        test = [match.value for match in parse('network[*].firewall[*].self.source_data').find(self.resources) if
                port in [port.value for port in parse('allowed[*].ports[*]').find(match.value)] and source_range in [
                    source_range.value for source_range in parse('sourceRanges[*]').find(match.value)]]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="DNS access is opend for all.")

    def test_check_ftp_open_access(self):
        """
        check FTP access from open netork
        """
        port = '20'
        port1 = '21'
        source_range = '0.0.0.0/0'
        test = [match.value for match in parse('network[*].firewall[*].self.source_data').find(self.resources) if (
                    port in [port.value for port in parse('allowed[*].ports[*]').find(match.value)] or port1 in [
                port.value for port in parse('allowed[*].ports[*]').find(match.value)]) and source_range in [
                    source_range.value for source_range in parse('sourceRanges[*]').find(match.value)]]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="FTP access is opend for all.")

    def test_check_mysql_open_access(self):
        """
        check MYSql access from open netork
        """
        port = '3306'
        source_range = '0.0.0.0/0'
        test = [match.value for match in parse('network[*].firewall[*].self.source_data').find(self.resources) if
                port in [port.value for port in parse('allowed[*].ports[*]').find(match.value)] and source_range in [
                    source_range.value for source_range in parse('sourceRanges[*]').find(match.value)]]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="MYSql access is opend for all.")

    def test_check_postgre_sql_open_access(self):
        """
        check PostGreSQL access from open netork
        """
        port = '5432'
        source_range = '0.0.0.0/0'
        test = [match.value for match in parse('network[*].firewall[*].self.source_data').find(self.resources) if
                port in [port.value for port in parse('allowed[*].ports[*]').find(match.value)] and source_range in [
                    source_range.value for source_range in parse('sourceRanges[*]').find(match.value)]]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="PostGreSQL access is opend for all.")

    def test_checkPostMSSQLOpenAccess(self):
        """
        check MSSQL access from open netork
        """
        port = '1433'
        source_range = '0.0.0.0/0'
        test = [match.value for match in parse('network[*].firewall[*].self.source_data').find(self.resources) if
                port in [port.value for port in parse('allowed[*].ports[*]').find(match.value)] and source_range in [
                    source_range.value for source_range in parse('sourceRanges[*]').find(match.value)]]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="MSSQL access is opend for all.")

    def test_check_rpc_call_open_access(self):
        """
        check RPCCall access from open netork
        """
        port = '135'
        source_range = '0.0.0.0/0'
        test = [match.value for match in parse('network[*].firewall[*].self.source_data').find(self.resources) if
                port in [port.value for port in parse('allowed[*].ports[*]').find(match.value)] and source_range in [
                    source_range.value for source_range in parse('sourceRanges[*]').find(match.value)]]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="RPCCall access is opend for all.")

    def test_check_smtp_open_access(self):
        """
        check SMTP access from open netork
        """
        port = '25'
        source_range = '0.0.0.0/0'
        test = [match.value for match in parse('network[*].firewall[*].self.source_data').find(self.resources) if
                port in [port.value for port in parse('allowed[*].ports[*]').find(match.value)] and source_range in [
                    source_range.value for source_range in parse('sourceRanges[*]').find(match.value)]]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="SMTP access is opend for all.")

    def test_check_ssh_open_access(self):
        """
        check SSH access from open netork
        """
        port = '22'
        source_range = '0.0.0.0/0'
        test = [match.value for match in parse('network[*].firewall[*].self.source_data').find(self.resources) if
                port in [port.value for port in parse('allowed[*].ports[*]').find(match.value)] and source_range in [
                    source_range.value for source_range in parse('sourceRanges[*]').find(match.value)]]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="SSH access is opend for all.")

    def test_check_icmp_open_access(self):
        """
        check ICMP access from open netork
        """
        port_name = 'icmp'
        source_range = '0.0.0.0/0'
        test = [match.value for match in parse('network[*].firewall[*].self.source_data').find(self.resources) if
                port_name in [port.value for port in
                              parse('allowed[*].IPProtocol').find(match.value)] and source_range in [source_range.value
                                                                                                     for source_range in
                                                                                                     parse(
                                                                                                         'sourceRanges[*]').find(
                                                                                                         match.value)]]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="ICMP access is opend for all.")

    def test_check_open_all_ports(self):
        """
        check all port is open or not
        """
        port_name = 'all'
        test = [match.value for match in parse('network[*].firewall[*].self.source_data').find(self.resources) if
                port_name in [port.value for port in parse('allowed[*].IPProtocol').find(match.value)]]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="All port is enabled.")

    def test_check_port_range(self):
        """
        check port ranges is open for all
        """
        source_range = '0.0.0.0/0'
        test = [match.value for match in parse('network[*].firewall[*].self.source_data').find(self.resources) if len(
            [port.value for port in parse('allowed[*].ports[*]').find(match.value) if
             len(port.value.split('-')) > 1]) and source_range in [source_range.value for source_range in
                                                                   parse('sourceRanges[*]').find(match.value)]]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="Port ranges are opend for all.")

    def test_firewall_logs(self):
        """
        check logs is enable or not for firewall
        """
        test = [match.value for match in
                parse('network[*].firewall[*].self.source_data.logConfig.enable').find(self.resources) if
                match.value in ['false', False]]
        flag = len(test) > 0
        self.assertEqual(False, flag, msg="Firewall rules doesn't have logs enabled.")

    def test_firewall_logs_meta_data(self):
        """
        check logs meta data is is enable or not for firewall
        """
        test = [match.value for match in
                parse('network[*].firewall[*].self.source_data.logConfig.metadata').find(self.resources) if
                match.value == 'INCLUDE_ALL_METADATA']
        flag = len(test) > 0
        print('test', test)
        self.assertEqual(False, flag, msg="Firewall logs shouldn't contain metadata logs.")
