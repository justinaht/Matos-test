# -*- coding: utf-8 -*-
from .config import PROVIDERS, PROVIDER_OBSERVE_MANAGER


class Observability:
    def __init__(self, provider, project_id, location, resource_name):
        """
        Initialize with set of required Observability data to fetch, process.

        Args:
            provider str: GCP, AWS or any.
            project_id str: Alpha numeric unique value identifying the project in the cloud infra.
            location str: Default cloud infra location, e.g us-east1, us-west1 etc.
            resource_name str: This can be like, cluster or VM or similar observability resource.
        """
        if provider not in PROVIDERS:
            raise Exception(f"Provider {provider} is not supported.")
        self.provider = provider
        self.project_id = project_id
        self.location = location
        self.resource = resource_name
        self._manager = None

    @property
    def manager(self):
        if not self._manager:
            MONITOR_RES_TYP = f"{self.provider}_{self.resource}"
            _manager = PROVIDER_OBSERVE_MANAGER.get(MONITOR_RES_TYP)
            if _manager:
                self._manager = _manager(self.project_id, self.location, self.resource)
        return self._manager

    def get_observability_details(self):
        """
        Get the observability details for the requested resource.
        # In progress.
        """
        app_observability = {
            "project": self.project_id,
            "location": self.location,
        }
        if self.manager:
            observability_info = self.manager.get_observability()
            app_observability.update(observability_info)
        return app_observability
