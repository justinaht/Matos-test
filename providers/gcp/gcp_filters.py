# -*- coding: utf-8 -*-
import time

from google.cloud.monitoring_v3.types import TimeInterval

from .gcp_config import FILTERS_ARGS, FILTERS_MAP, K8S_TYP, RESOURCE_TYPE_FACTOR


class ResourceMetricFilterInfo:
    def __init__(
        self,
        metric_type,
        resource_type,
        resource_name,
        location=None,
        zone=None,
        node_value=None,
    ):
        """
        Initialize the Resource Metrics filter query to execute on listTimeSeries based call.

        Args:
            metric_type str: Type of observability parameter consider to calculate the utilization of that resource.
            resource_type str: Kind of resource being requested to observe. e.g. k8s_node, container, instance etc.
            location/zone str: Resource availability or existence.
            Instance will help to construce the filter to get the monitor data.
        """
        self.metric_type = metric_type
        self.resource_type = resource_type
        self.resource_name = resource_name
        self.location = location
        self.zone = zone
        self.node_value = node_value

    def get_factor_and_filter(self):
        """
        Construct the filter to apply on Lists time series to get the Metric descriptors.
        """
        resource_type = FILTERS_MAP.get(self.resource_type)
        filter_args = FILTERS_ARGS.get(self.resource_type)
        filter_values = [getattr(self, field) for field in filter_args]
        resource_filter = resource_type.format(*filter_values)
        return resource_filter, RESOURCE_TYPE_FACTOR[self.resource_type]

    def get_time_interval(self):
        now = time.time()
        seconds = int(now)
        nanos = int((now - seconds) * 10 ** 9)
        offset_time = 60 if self.resource_type in K8S_TYP else 240
        return TimeInterval(
            {
                "end_time": {"seconds": seconds, "nanos": nanos},
                "start_time": {"seconds": (seconds - offset_time), "nanos": nanos},
            }
        )


def get_ephemeral_storage_metrics(metric_info):
    used_bytes = metric_info.get("node.ephemeral_storage_used_bytes")
    total_bytes = metric_info.get("node.ephemeral_storage_total_bytes")
    free_inodes = metric_info.get("node.ephemeral_storage_free_inodes")
    total_inodes = metric_info.get("node.ephemeral_storage_total_inodes")
    return {
        "used_bytes": used_bytes,
        "total_bytes": total_bytes,
        "free_inodes": free_inodes,
        "total_inodes": total_inodes,
        "unit": "bytes",
    }


def get_pid_metrics(metric_info):
    return {
        "pid_used": metric_info.get("node.pid_used"),
        "pid_limit": metric_info.get("node.pid_limit"),
    }
