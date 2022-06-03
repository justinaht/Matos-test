# -*- coding: utf-8 -*-
# from .aws import AWSResourceManager, AWSObservation
from .aws import AWSResourceManager
from .gcp import GCPResourceManager
from .azure import AzureResourceManager
from .aws.aws_discovery import AWSDiscovery
from .gcp.gcp_discovery import GCPDiscovery
from .azure.azure_discovery import AzureDiscovery

PROVIDER_RESOURCE_MANAGER = {
    "gcp": GCPResourceManager,
    "aws": AWSResourceManager,
    'azure': AzureResourceManager,
}

DISCOVERY_MANAGER = {
    "aws": AWSDiscovery,
    "gcp": GCPDiscovery,
    "azure": AzureDiscovery
}

PROVIDER_OBSERVE_MANAGER = {
    # "gcp": GCPObservation,
    # "aws": AWSObservation
}

PROVIDERS = PROVIDER_RESOURCE_MANAGER.keys()
