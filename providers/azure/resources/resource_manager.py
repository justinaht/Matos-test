# -*- coding: utf-8 -*-
from structlog import get_logger

from providers.azure.azure_connection import Azure
# from providers.azure.azure_config import INSTANCE_TYPE_CONFIG
from datetime import datetime, timedelta
import time
from datetime import datetime, timedelta
import json
import yaml
import ruamel.yaml
from kubernetes import client as kclient, config as kconfig
import base64

logger = get_logger(__file__)


class AzureResourceManager:
    def __init__(self,
                 **kwargs,
                 ) -> None:
        print("Azure Resource Manage __init__ Method")

    def get_assets_inventory(
            self, resource, **kwargs
    ):
        RESOURCE_TYPES = {
            "cluster": Cluster,
            "instance": Instance,
            "storage": Storage,
            "network": Network,
            "sql": SQL,
        }

        log = logger.new()
        # print(resource['type'], "==== resource type")

        # try:
        Resource = RESOURCE_TYPES.get(resource['type'])
        if not Resource:
            log.info("Requested resource_type is not supported.")
            return
        try:
            cloud_resource = Resource(
                resource,
            )

            resource_details = cloud_resource.get_resource_inventory()
        except Exception as ex:
            raise Exception(ex)

        if resource_details:
            resource.update(details=resource_details)

        return resource


class Cluster(Azure):

    def __init__(self,
                 resource,
                 **kwargs,
                 ) -> None:
        try:
            super(Cluster, self).__init__()
            self.conn = self.client("cluster")
            self.resource = resource
        except Exception as ex:
            raise Exception(ex)

    def replace_none_with(self, d, replacement=0):
        retval = {}
        for key, val in d.items():
            if val is None:
                retval[key] = replacement
            elif isinstance(val, dict):
                retval[key] = self.replace_none_with(val, replacement)
            elif isinstance(val, datetime):
                retval[key] = val.strftime("%m/%d/%Y, %H:%M:%S")
            elif isinstance(val, list):
                emtlist = []
                for lt in val:
                    if isinstance(lt, dict):
                        emtlist.append(self.replace_none_with(lt, replacement))
                retval[key] = emtlist
            else:
                retval[key] = val
        return retval

    def get_resource_inventory(self):
        """
        Fetches cluster details.

        Args:
        cluster_name: name of the eks instance.

        return: dictionary object.
        """
        cluster_details = self.get_cluster_details()
        return cluster_details

    def get_cluster_client(self, cluster_info):
        rg_name = cluster_info.get('id', '').split('/')[-5]
        k8s_name = cluster_info.get('name')
        kubeconfig = self.conn.managed_clusters.list_cluster_admin_credentials(rg_name, k8s_name).kubeconfigs[0]
        k8s_kubeconfig = base64.b64decode((kubeconfig.as_dict())['value'])
        obj_data = ruamel.yaml.safe_load(k8s_kubeconfig)
        with open(f'{k8s_name}.yml', 'w') as f:
            yaml.dump(obj_data, f)
        kube_client = kconfig.load_kube_config(f'{k8s_name}.yml')
        k8s_client = kclient.ApiClient(kube_client)
        k8s_client_v1 = kclient.CoreV1Api(k8s_client)

        return k8s_client_v1

    def get_cluster_details(self):
        resources = [self.scrub(item) for item in self.conn.managed_clusters.list()]
        resources = [{
            **resource,
            "pod": self.replace_none_with(
                self.get_cluster_client(resource).list_pod_for_all_namespaces().to_dict(),
                replacement='None').get('items', []),
            "service": self.replace_none_with(
                self.get_cluster_client(resource).list_service_for_all_namespaces().to_dict(),
                replacement='None').get('items', []),
        } for resource in resources if resource.get('name', '') == self.resource.get('name')]
        return resources[0] if len(resources) > 0 else self.resource


class Instance(Azure):
    def __init__(self,
                 resource: dict,
                 **kwargs,
                 ) -> None:
        """
        """
        try:
            super(Instance, self).__init__()
            self.conn = self.client("instance")
            self.resource = resource

        except Exception as ex:
            raise Exception(ex)

    def get_resource_inventory(self):
        """
        Fetches instance details.

        Args:
        instance_id (str): Ec2 instance id.
        return: dictionary object.
        """
        resources = [self.scrub(item) for item in self.conn.virtual_machines.list_all()]
        resources = [resource for resource in resources if resource.get('name', '') == self.resource.get('name')]
        return resources[0] if len(resources) > 0 else self.resource


class Storage(Azure):
    def __init__(self,
                 resource: dict,
                 **kwargs,
                 ) -> None:
        """
        """
        try:
            super(Storage, self).__init__()
            self.conn = self.client("storage")
            self.resource = resource

        except Exception as ex:
            raise Exception(ex)

    def get_resource_inventory(self):
        """
        Fetches instance details.

        Args:
        instance_id (str): Ec2 instance id.
        return: dictionary object.
        """
        resources = [self.scrub(item) for item in self.conn.storage_accounts.list()]
        resources = [resource for resource in resources if resource.get('name', '') == self.resource.get('name')]
        return resources[0] if len(resources) > 0 else self.resource


class Network(Azure):
    def __init__(self,
                 resource: dict,
                 **kwargs,
                 ) -> None:
        """
        """
        try:
            super(Network, self).__init__()
            self.conn = self.client("network")
            self.resource = resource

        except Exception as ex:
            raise Exception(ex)

    def get_resource_inventory(self):
        """
        Fetches instance details.

        Args:
        instance_id (str): Ec2 instance id.
        return: dictionary object.
        """
        resources = [self.scrub(item) for item in self.conn.virtual_networks.list_all()]
        resources = [resource for resource in resources if resource.get('name', '') == self.resource.get('name')]
        return resources[0] if len(resources) > 0 else self.resource


class SQL(Azure):
    def __init__(self,
                 resource: dict,
                 **kwargs,
                 ) -> None:
        """
        """
        try:
            super(SQL, self).__init__()
            self.conn = self.client("sql")
            self.resource = resource

        except Exception as ex:
            raise Exception(ex)

    def get_resource_inventory(self):
        """
        Fetches instance details.

        Args:
        instance_id (str): Ec2 instance id.
        return: dictionary object.
        """

        resources = [self.scrub(item) for item in self.conn.servers.list()]
        resources = [resource for resource in resources if resource.get('name', '') == self.resource.get('name')]
        return resources[0] if len(resources) > 0 else self.resource
