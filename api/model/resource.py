class ResourceModel:
    def __init__(self, resource):
        self.cluster = resource.get('cluster')
        self.instance = resource.get('instance')
        self.network = resource.get('network')
        self.storage = resource.get('storage')
        self.serviceAccount = resource.get('serviceAccount')
        self.sql = resource.get('sql')
        self.iam = resource.get('iam')
        self.disk = resource.get('disk')
        self.snapshot = resource.get('snapshot')
        self.log_monitor = resource.get('log_monitor')
        self.kms = resource.get('kms')
        self.policy = resource.get('policy')
        self.no_sql = resource.get('no_sql')
        self.eip = resource.get('eip')

class ResourceClusterSelfModel:
    def __init__(self, resource):
        self.name = resource.get('name')
        # self.display_name = resource.get('display_name')
        self.logging = resource.get('logging')
