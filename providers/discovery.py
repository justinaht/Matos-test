from .config import DISCOVERY_MANAGER


class Discovery:

    def __init__(self,
                 provider: str,
                 **kwargs,
                 ) -> None:
        """
        """
        self.provider = provider
        self.kwargs = kwargs

        if provider not in DISCOVERY_MANAGER:
            raise NotImplementedError("Provider not implemented yet")

        self.manager = DISCOVERY_MANAGER[provider](
            **kwargs,
        )

    def find_resources(self, **kwargs):
        """
        """

        return self.manager.find_resources(**kwargs)

    def find_resources_cluster_self(self, cluster_name, **kwargs):
        """
        """
        return self.manager.find_resources_cluster_self(cluster_name, **kwargs)

    def update_cluster_logging(self, cluster_name, logging_data, **kwargs):
        """
        """
        return self.manager.update_cluster_logging(cluster_name, logging_data, **kwargs)
        
