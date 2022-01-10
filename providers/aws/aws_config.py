# -*- coding: utf-8 -*-

RESOURCE_CONFIG = {
    "eks": ("get_cluster_details", "client"),
    "ec2": ("get_instance_details", "client"),
}


INSTANCE_TYPE_CONFIG = {
    "t2.nano": {"memory": 0.5, "cpu": 1},
    "t2.micro": {"memory": 1, "cpu": 1},
    "t2.small": {"memory": 2, "cpu": 1},
    "t2.medium": {"memory": 4, "cpu": 2},
    "t2.large": {"memory": 8, "cpu": 2},
    "t2.xlarge": {"memory": 16, "cpu": 4},
    "t2.2xlarge": {"memory": 32, "cpu": 8},
}


class AWSConfig:

    filter_name_map = {
        "instance_id": "InstanceId",
    }
