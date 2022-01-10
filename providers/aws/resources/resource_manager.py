# -*- coding: utf-8 -*-
from structlog import get_logger

from providers.aws.connection import AWS
from providers.aws.aws_config import INSTANCE_TYPE_CONFIG
from datetime import datetime, timedelta
import time
from kubernetes import client as kclient
from datetime import datetime, timedelta
from awscli.customizations.eks.get_token import STSClientFactory, TokenGenerator, TOKEN_EXPIRATION_MINS

logger = get_logger(__file__)


class AWSResourceManager:
    def __init__(self,
                 **kwargs,
                 ) -> None:
        print("AWS Resource Manage __init__ Method")

    def get_assets_inventory(
        self, resource, **kwargs
    ):
        RESOURCE_TYPES = {
            "eks": Cluster,
            "cluster": Cluster,
            "ec2": Instance,
            "instance": Instance,
        }

        log = logger.new()

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
        # except Exception as ex:
        #     log.error("Error while fetching resource details.",
        #               error_message=str(ex))

        return resource


class Cluster(AWS):

    def __init__(self,
                 resource,
                 **kwargs,
                 ) -> None:
        try:
            super(Cluster, self).__init__()
            self.conn = self.client("eks")
            self.cluster_names = [resource['name']]
        except Exception as ex:
            raise Exception(ex)

    def get_cluster_client(self,
                           cluster_name,
                           cluster_host,
                           ):
        """
        """

        work_session = self.session._session
        client_factory = STSClientFactory(work_session)

        def get_expiration_time():
            token_expiration = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION_MINS)
            return token_expiration.strftime('%Y-%m-%dT%H:%M:%SZ')

        def get_token(cluster_name: str, role_arn: str = None) -> dict:
            sts_client = client_factory.get_sts_client(role_arn=role_arn)
            token = TokenGenerator(sts_client).get_token(cluster_name)
            return {
                "kind": "ExecCredential",
                "apiVersion": "client.authentication.k8s.io/v1alpha1",
                "spec": {},
                "status": {
                        "expirationTimestamp": get_expiration_time(),
                        "token": token
                }
            }

        token = get_token(cluster_name)['status']['token']
        conf = kclient.Configuration()

        conf.host = cluster_host + ':443'
        conf.verify_ssl = False
        conf.api_key = {'authorization': "Bearer " + token}
        k8s_client = kclient.ApiClient(conf)
        k8s_client_v1 = kclient.CoreV1Api(k8s_client)

        return k8s_client_v1

    def get_resource_inventory(self):
        """
        Fetches cluster details.

        Args:
        cluster_name: name of the eks instance.

        return: dictionary object.
        """
        cluster_details = self.get_cluster_details()
        return cluster_details

    def get_object_count(self,
                         object_types,
                         time_period=100*60,
                         filters={},
                         ):
        """
        """

        logs = self.client('logs')

        then = (datetime.utcnow() - timedelta(seconds=time_period)).timestamp()
        now = datetime.utcnow().timestamp()

        log_groups = [
            '/aws/containerinsights/wpcon/performance',
            '/aws/containerinsights/wpcon/host',
            '/aws/containerinsights/wpcon/application',
            '/aws/containerinsights/wpcon/dataplane',
        ]

        map1 = {
            'pod': 'kubernetes.pod_name',
            'namespace': 'kubernetes.namespace_name',
            'container': 'kubernetes.container_name',
            'service': 'kubernetes.service_name',
        }

        map2 = {
            'pod': 'PodName',
            'namespace': 'Namespace',
            'node': 'NodeName',
            'cluster': 'ClusterName'
        }

        object_names = [(map2.get(o) or map1.get(o) or o)
                        for o in object_types]

        fields = ', '.join(object_names)
        field_query = f"fields {fields}"
        count_query = ", ".join([f"count_distinct({o})" for o in object_names])

        if filters:
            filter_queries = [f'filter({map2.get(x) or map1.get(x) or x}="{y}")'
                              for x, y in filters.items()]
            filter_string = ' | '.join(filter_queries)
            query = f'{field_query} | {filter_string} | {count_query}'
        else:
            query = f'{field_query} | {count_query}'

        query_response = logs.start_query(
            startTime=int(then),
            endTime=int(now),
            queryString=query,
            logGroupNames=log_groups)

        while True:
            query_result = logs.get_query_results(
                queryId=query_response['queryId'])
            if query_result['status'] == 'Running':
                time.sleep(1)
                continue

            break

        rev = {x: y for y, x in map1.items()}
        rev.update({x: y for y, x in map2.items()})

        retdict = {}

        for res in query_result['results'][0]:
            o = res['field'][15:][:-1]
            o = rev.get(o) or o
            v = int(res['value'])
            retdict[o] = v

        return retdict

    def add_cluster_objects_from_k8s(self,
                                     cluster_details,
                                     ):
        """
        """

        name = cluster_details['name']
        endpoint = cluster_details['endpoint']
        k8s_client = self.get_cluster_client(name, endpoint)

        function_map = {
            'pod': k8s_client.list_pod_for_all_namespaces,
            'namespace': k8s_client.list_namespace,
            'node': k8s_client.list_node,
            'service': k8s_client.list_service_account_for_all_namespaces,
        }

        object_map = {}

        def append_objects(object_type, objects):
            for object in objects.items:
                object_list = object_map.get(object_type, [])
                object_name = object.metadata.name
                object_namespace = getattr(object.metadata, 'namespace', None)

                object_details = {
                    'name': object_name
                }

                if object_namespace:
                    object_details.update(namespace=object_namespace)

                if object_type == 'node':
                    try:
                        instance_id = object.spec.provider_id.split('/')[-1]
                        object_details.update(instance_id=instance_id)
                    except:
                        pass

                object_list.append(object_details)
                object_map[object_type] = object_list

        for object_type, function in function_map.items():
            try:
                objects = function()
                append_objects(object_type, objects)

                if object_type == 'pod':
                    object_list = object_map.get('container', [])
                    object_list.extend(
                        [{'name': c.name}
                         for object in objects
                         for c in object.spec.containers]
                    )
                    object_map['container'] = object_list

            except:
                pass

        cluster_details.update(object_map)

    def add_cluster_objects_from_cloudwatch(self,
                                            cluster_details,
                                            ):
        """
        """

        name = cluster_details['name']

        object_list = ['pod', 'namespace', 'node', 'container', 'service']

        object_count = self.get_object_count(
            object_list, filters={'cluster': name})

        for object, count in object_count.items():
            cluster_details[f"{object}_count"] = count

        return cluster_details

    def get_cluster_details(self, fetch_objects=True):

        def add_objects(cluster_details):
            try:
                self.add_cluster_objects_from_k8s(cluster_details)
            except:
                try:
                    self.add_cluster_objects_from_cloudwatch(cluster_details)
                except:
                    pass

        if self.cluster_names and len(self.cluster_names) == 1:
            name = self.cluster_names[0]
            cluster_details = self.conn.describe_cluster(name=name)
            cluster_details = cluster_details.get("cluster")
            if cluster_details and fetch_objects:
                add_objects(cluster_details)
            return cluster_details

        clusters = self.conn.list_clusters()
        clusters_details = []

        for name in clusters.get('clusters', []):

            if self.cluster_names and name not in self.cluster_names:
                continue

            data = self.conn.describe_cluster(name=name)
            cluster = data.get('cluster')

            if cluster and fetch_objects:
                add_objects(cluster)

            clusters_details.append(cluster)

        return clusters_details


class Instance(AWS):
    def __init__(self,
                 resource: dict,
                 **kwargs,
                 ) -> None:
        """
        """
        try:
            super(Instance, self).__init__()
            self.conn = self.client("ec2")
            self.instance_ids = resource.get('instance_id') or resource.get('name')

            if self.instance_ids:
                self.instance_ids = [self.instance_ids]
        except Exception as ex:
            raise Exception(ex)

    def get_resource_inventory(self):
        """
        Fetches instance details.

        Args:
        instance_id (str): Ec2 instance id.
        return: dictionary object.
        """
        instances_details = self.get_describe_instances()
        instances_details = self.get_instance_details(instances_details)
        return instances_details

    def get_describe_instances(self):
        if self.instance_ids:
            instance_details = self.conn.describe_instances(
                InstanceIds=self.instance_ids
            )
        else:
            instance_details = self.conn.describe_instances()

        return instance_details

    def get_instance_details(self, instances_details):
        reservations = instances_details.get("Reservations")
        if reservations and isinstance(reservations, list):
            instances = [
                instance.get("Instances")[0]
                for instance in reservations
                if instance.get("Instances")
            ]
            for instance_details in instances:
                self.update_volume_details(instance_details)
                instance_type = instance_details.get("InstanceType")
                instance_config = INSTANCE_TYPE_CONFIG.get(instance_type)
                instance_details["InstanceMemory"] = {
                    "total": instance_config["memory"] if instance_config else 0,
                    "unit": "GB",
                }
                if self.instance_ids and\
                        instance_details.get("InstanceId") in self.instance_ids:
                    return instance_details
            return instances

    def update_volume_details(self, instance_details):
        """
        Update instance details with additional volumes data.
        """
        volume_ids = [
            vol["Ebs"]["VolumeId"] for vol in instance_details["BlockDeviceMappings"]
        ]
        volumes = self.conn.describe_volumes(VolumeIds=volume_ids)
        volumes = volumes.get("Volumes")
        total_size = 0
        volumes_data = []
        if volumes:
            for vol in volumes:
                volumes_data.append(
                    {
                        "VolumeId": vol.get("VolumeId"),
                        "AvailabilityZone": vol.get("AvailabilityZone"),
                        "Size": vol.get("Size"),
                        "VolumeType": vol.get("VolumeType"),
                        "State": vol.get("State"),
                        "Iops": vol.get("Iops"),
                        "DeviceName": vol["Attachments"][0]["Device"] if len(vol['Attachments']) else '',
                    }
                )
                total_size += vol.get("Size")
            if volumes_data:
                instance_details["BlockDeviceMappings"] = {
                    "DiskSize": {"total": total_size, "unit": "GB"},
                    "Volumes": volumes_data,
                }
