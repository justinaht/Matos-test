from .connection import AWS


class AWSDiscovery(AWS):
    """
    """

    def __init__(self,
                 **kwargs) -> None:
        try:
            super().__init__(**kwargs)
            self.eks = self.client('eks')
            self.ec2 = self.client('ec2')
        except Exception as ex:
            raise Exception(ex)

    def get_instances(self):
        """
        """

        resources = self.ec2.describe_instances()
        reservations = resources['Reservations']

        instances = []

        for reservation in reservations:
            for instance in reservation.get('Instances', []):
                instances.append({
                    'type': 'instance',
                    'instance_id': instance['InstanceId'],
                    'name': instance['InstanceId'],
                    'location': instance['Placement']['AvailabilityZone']
                })

        return instances

    def get_clusters(self):
        """
        """

        clusters = self.eks.list_clusters()
        clusters = clusters['clusters']

        cluster_resources = []

        for cluster in clusters:
            cluster_details = self.eks.describe_cluster(name=cluster)
            cluster_details = cluster_details['cluster']
            cluster_resources.append({
                'name': cluster_details['name'],
                'type': 'cluster',
                'location': cluster_details['endpoint']
                .replace('.eks.amazonaws.com', '').split('.')[-1]
            })
        
        return cluster_resources

    def find_resources(self, **kwargs):
        """
        """

        resources = []

        resources.extend(self.get_clusters())
        resources.extend(self.get_instances())

        return resources
