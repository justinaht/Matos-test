# -*- coding: utf-8 -*-
# from .aws import AWSResourceManager, AWSObservation
from .aws import AWSResourceManager
from .gcp import GCPResourceManager
from .aws.aws_discovery import AWSDiscovery
from .gcp.gcp_discovery import GCPDiscovery

PROVIDER_RESOURCE_MANAGER = {
    "gcp": GCPResourceManager,
    "aws": AWSResourceManager,
}

DISCOVERY_MANAGER = {
    "aws": AWSDiscovery,
    "gcp": GCPDiscovery,
}

PROVIDER_OBSERVE_MANAGER = {
    # "gcp": GCPObservation,
    # "aws": AWSObservation
}

PROVIDERS = PROVIDER_RESOURCE_MANAGER.keys()
