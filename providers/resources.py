from .config import PROVIDERS, PROVIDER_RESOURCE_MANAGER
from .gcp.gcp_config import RESOURCE_TYPE_REQUESTS


# TODO: Logging needs to be initialise and apply.


class Resource:
    def __init__(self,
                 provider: str,
                 ):
        if provider not in PROVIDERS:
            raise Exception(f"Provider {provider} is not supported.")
        self.provider = provider
        self._manager = None

    @property
    def manager(self):
        if not self._manager:
            _manager = PROVIDER_RESOURCE_MANAGER.get(self.provider)
            if _manager:
                try:
                    self._manager = _manager()
                except Exception as ex:
                    raise Exception(ex)
                # if self.provider == "gcp":
                # else:
                #     self._manager = _manager()
        return self._manager

    def get_resource_inventory(
        self,
        resource_list
    ):
        """
        """

        if self.manager:
            resources = {}
            if self.provider == 'gcp':
                try:
                    for resource_type in RESOURCE_TYPE_REQUESTS.keys():
                        resources[resource_type] = self.manager.get_assets_inventory({"type": resource_type})
                except Exception as ex:
                    raise Exception(ex)
            elif self.provider != 'aws':
                for resource_type in RESOURCE_TYPE_REQUESTS.keys():
                    resources[resource_type] = [self.manager.get_assets_inventory(resource) for resource in resource_list if resource['type'] == resource_type]

            return resources
