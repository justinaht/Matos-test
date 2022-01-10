from itertools import groupby


def aws_cluster(resource, provider):
    """
    """

    cluster = selfish({
        "display_name": from_dict(resource, "name"),
        "name": from_dict(resource, "name"),
        "arn": from_dict(resource, "arn"),
        "endpoint": from_dict(resource, 'endpoint'),
        "resources_vpc_config": from_dict(resource, "resourcesVpcConfig"),
        "created_time": from_dict(resource, 'createdAt'),
        "status": from_dict(resource, "status"),
        "tags": from_dict(resource, "tags"),
        "version": from_dict(resource, "version"),
        "roleArn": from_dict(resource, "roleArn"),
        "platformVersion": from_dict(resource, "platformVersion"),
        "namespace": from_dict(resource, "namespace"),
        "identity": from_dict(resource, "identity"),
        "kubernetesNetworkConfig": from_dict(resource, "kubernetesNetworkConfig"),
        "logging": from_dict(resource, "logging"),
        "region": from_dict(resource, "zone")
    })

    add_child(aws_cluster_pod, "pod", "pod", resource, cluster, provider)
    add_child(aws_cluster_service, "service", "service", resource, cluster, provider)
    add_child(aws_cluster_node, "node", "node", resource, cluster, provider)

    return cluster


def aws_cluster_pod(resource):
    """
    """

    return selfish({
        'name': resource['name'],
        'namespace': resource['namespace'],
    })


def aws_cluster_node(resource):
    """
    """

    return selfish({
        'name': resource['name'],
        'instance_id': resource['instance_id']
    })


def aws_cluster_service(resource):
    """
    """

    return selfish({
        'name': resource['name'],
        'namespace': resource['namespace']
    })


def aws_instance(resource, provider):
    """
    """

    return selfish({
        "instance_id": from_dict(resource, "InstanceId"),
        "display_name": from_dict(resource, "InstanceId"),
        "instance_type": from_dict(resource, "InstanceType"),
        "zone": from_dict(resource, "Placement", "AvailabilityZone"),
        "network_interfaces": from_dict(resource, "NetworkInterfaces"),
        "tags": from_dict(resource, "Tags"),
        "subnet_id": from_dict(resource, "SubnetId"),
        "memory": from_dict(resource, "InstanceMemory"),
        "image_id": from_dict(resource, "ImageId"),
        "launch_time": from_dict(resource, "LaunchTime"),
        "cpu_option": from_dict(resource, "CpuOptions"),
        "block_device_mappings": from_dict(resource, "BlockDeviceMappings")
    })


def gcp_cluster(resource, provider):
    """
    Add properties as required from the API result.
    """

    cluster_details = resource['cluster']
    clusters = []

    if isinstance(cluster_details, list):
        for cluster_item in cluster_details:
            cluster = selfish({
                "name": from_dict(cluster_item, "resource", "data", "name"),
                "display_name": from_dict(cluster_item, "resource", "data", "name"),
                "description": from_dict(cluster_item, "resource", "data", "description"),
                "self_link": from_dict(cluster_item, "resource", "data", "selfLink"),
                "region": from_dict(cluster_item, "resource", "data", "zone"),
                "endpoint": from_dict(cluster_item, "resource", "data", "endpoint"),
                "create_time": from_dict(cluster_item, "resource", "data", "createTime"),
                "status": from_dict(cluster_item, 'resource', 'data', 'status'),
                "source_data": from_dict(cluster_item, 'resource', 'data'),
            })

            add_child(gcp_cluster_pod, "pods", "pod", resource, cluster, provider)
            add_child(gcp_cluster_service, "services", "service", resource, cluster, provider)
            add_child(gcp_cluster_node, "nodes", "node", resource, cluster, provider)

            clusters.append(cluster)

    return clusters


def gcp_cluster_node(resource):
    """
    """

    return selfish({
        "name": from_dict(resource, "resource", "data", "metadata", "name"),
        "display_name": from_dict(resource, "resource", "data", "metadata", "name"),
        "self_link": from_dict(resource, "resource", "data", "metadata", "selfLink"),
        "cluster_name": from_dict(resource, "cluster_name"),
        "create_time": from_dict(resource, "resource", "data", "metadata", "creationTimestamp"),
        "status": from_dict(resource, "resource", "data", "status"),
        "source_data": from_dict(resource, "resource", "data")
    })


def gcp_cluster_pod(resource):
    """
    """

    return selfish({
        "name": from_dict(resource, "resource", "data", "metadata", "name"),
        "display_name": from_dict(resource, "resource", "data", "metadata", "name"),
        "cluster_name": from_dict(resource, "cluster_name"),
        "node_name": from_dict(resource, "resource", "data", "spec", "nodeName"),
        "namespace": from_dict(resource, "resource", "data", "metadata", "namespace"),
        "create_time": from_dict(resource, "resource", "data", "metadata", "creationTimestamp"),
        "status": from_dict(resource, "resource", "data", "status"),
        "source_data": from_dict(resource, "resource", "data"),
    })


def gcp_cluster_service(resource):
    """
    """

    return selfish({
        "name": from_dict(resource, "resource", "data", "metadata", "name"),
        "cluster_name": from_dict(resource, "cluster_name"),
        "namespace": from_dict(resource, "resource", "data", "metadata", "namespace"),
        "create_time": from_dict(resource, "resource", "data", "metadata", "creationTimestamp"),
        "status": from_dict(resource, "resource", "data", "status"),
        "source_data": from_dict(resource, "resource", "data")
    })


def gcp_instance(resource, provider):
    """
    """

    instance_details = resource['instance']

    instances = []
    if isinstance(instance_details, list):
        for instance_item in instance_details:
            instances.append(selfish({
                "instance_id": from_dict(instance_item, "resource", "data", "id"),
                "name": from_dict(instance_item, "resource", "data", "name"),
                "display_name": from_dict(instance_item, "resource", "data", "name"),
                "self_link": from_dict(instance_item, "resource", "data", "selfLink"),
                "create_time": from_dict(instance_item, "resource", "data", "creationTimestamp"),
                "status": from_dict(instance_item, "resource", "data", "status"),
                "source_data": from_dict(instance_item, "resource", "data"),
                "zone": from_dict(instance_item, "resource", "data", "zone")
            }))
    return instances


cloud_resource_mappers = {
    'aws': {
        'cluster': aws_cluster,
        'cluster_pod': None,
        'cluster_service': None,
        'cluster_node': None,
        'instance': aws_instance,
    },
    'gcp': {
        'cluster': gcp_cluster,
        'cluster_pod': None,
        'cluster_service': None,
        'cluster_node': None,
        'instance': gcp_instance,
    }
}


def from_dict(data, *paths, raise_error=False):
    """
    """

    last_value = data

    for current_path in paths:

        if isinstance(last_value, (list, tuple)):

            if not isinstance(current_path, int):
                if raise_error:
                    raise KeyError(f"{current_path} should be a integer,"
                                   " target value is a sequence")
                else:
                    return

            last_value = last_value[current_path]
            continue

        elif isinstance(last_value, dict):

            if current_path not in last_value:
                if raise_error:
                    raise KeyError(f"{current_path} is not present in target")
                else:
                    return

            last_value = last_value[current_path]
            continue

        if raise_error:
            raise KeyError(f"{type(last_value)} is not "
                           f"accessible with key {current_path}")
        else:
            return

    return last_value


def selfish(data):
    return {
        "self": data
    }


def check_support(provider, res_type):
    if provider not in cloud_resource_mappers:
        raise NotImplementedError(
            f"{provider} cloud provider is not supported yet")

    if res_type not in cloud_resource_mappers[provider]:
        raise NotImplementedError(f"{res_type} resource type is"
                                  f" not yet supported for {provider}")


def add_child(child_mapper,
              source_key,
              target_key,
              source_data,
              target_data,
              provider='gcp'
              ):
    """
    """

    if source_key not in source_data:
        return

    try:
        data = source_data[source_key]

        if not data:
            return

        if isinstance(data, (list, tuple, set)):
            mapped = [child_mapper(s) for s in data if from_dict(s, "cluster_name") == target_data['self']['name'] and provider == 'gcp' or provider == 'aws']
        else:
            mapped = child_mapper(data) if from_dict(data, "cluster_name") == target_data['self']['name'] and provider == 'gcp' or provider == 'aws' else None

        target_data.update({target_key: mapped})
    except:
        return


def mapper(provider, res_type, resource):
    """
    """

    res_mapper = cloud_resource_mappers[provider][res_type]

    if isinstance(resource, (list, tuple, set)):
        return [res_mapper(r, provider) for r in resource]

    return res_mapper(resource, provider)


def group_resources(resources):
    """
    """

    def key(resource):
        return resource['type']

    resources.sort(key=key)

    return {res_type: list(group)
            for res_type, group in groupby(resources, key=key)}


def reform_resources(provider, resources):
    """
    """

    retdict = {}
    if isinstance(resources, dict):
        res_type = resources['type']
        details = resources.get('details')
        if res_type == 'cluster' and provider == 'aws':
            details['zone'] = resources['location']

        if not details:
            return retdict

        try:
            check_support(provider, res_type)
        except NotImplementedError:
            details = {'self': details}
        else:
            details = mapper(provider, res_type, details)

        retdict[res_type] = details

    return retdict
