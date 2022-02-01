class ResourceModel:
    def __init__(self, resource):
        self.cluster = resource['cluster']
        self.instance = resource['instance']
        self.network = resource['network']
        self.storage = resource['storage']
        self.serviceAccount = resource['serviceAccount']
        self.sql = resource['sql']
