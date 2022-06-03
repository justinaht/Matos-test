from google.cloud import asset_v1p5beta1
from google.protobuf.json_format import MessageToDict
from googleapiclient import discovery
from .base import BaseGCPManager
from .gcp_config import ASSET_TYPES

INVERTED_TYPES = {x: y for y, x in ASSET_TYPES.items()}


class GCPDiscovery(BaseGCPManager):
    """
    """

    def __init__(self,
                 **kwargs,
                 ):
        super().__init__(

            **kwargs)

        self.SCOPES = []
        self.client = asset_v1p5beta1.AssetServiceClient(
            credentials=self.credentials)
        self.content_type = asset_v1p5beta1.ContentType.RESOURCE

    def get_projects(self):
        """
        """

        service = discovery.build('cloudresourcemanager', 'v1',
                                  credentials=self.credentials)
        request = service.projects().list()
        response = request.execute()

        return [x['projectId'] for x in response['projects']]

    def get_resources(
        self,
        project_id: str,
        *asset_types,
    ):

        request = {
            "asset_types": asset_types,
            "parent": f"projects/{project_id}",
            "content_type": self.content_type
        }

        assets = []
        next_page_token = None

        while True:

            if next_page_token:
                request["page_token"] = next_page_token

            response = self.client.list_assets(request=request)
            response_dict = MessageToDict(response._pb)
            page_assets = response_dict.get("assets") or []
            assets.extend(page_assets)

            next_page_token = response_dict.get("nextPageToken")

            if not next_page_token:
                break

        return assets

    def get_instances(self, project_id):
        """
        """

        resources = self.get_resources(project_id, INVERTED_TYPES['instance'])
        instances = []

        for resource in resources:
            instances.append({
                'type': 'instance',
                'name': resource['resource']['data']['name'],
                'instance_id': resource['resource']['data']['id'],
                'project_id': project_id,
                'location': resource['resource']['data']['zone'].split('/')[-1],
            })

        return instances

    def get_clusters(self, project_id):
        """
        """

        resources = self.get_resources(project_id, INVERTED_TYPES['cluster'])
        clusters = []

        for resource in resources:
            clusters.append({
                'type': 'cluster',
                'name': resource['resource']['data']['name'],
                'project_id': project_id,
                'location': resource['resource']['data']['zone'],
            })

        return clusters

    def find_resources(self, project_ids=[], **kwargs):
        """
        """

        if not project_ids:
            project_ids = self.get_projects()

        resources = []

        for project_id in project_ids:

            resources.extend(self.get_clusters(project_id))
            resources.extend(self.get_instances(project_id))

        return resources
