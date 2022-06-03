
from http import HTTPStatus
import json

from api.model.exception import ExceptionModel
from api.model.resource import ResourceClusterSelfModel
from api.schema.exception import ExceptionSchema
from api.schema.resource import ResourceClusterSelfSchema
from flask import Blueprint, request
from flasgger import swag_from
from services.resource_service import ResourceClusterSelfService

resource_cluster_self_api = Blueprint('cluster', __name__)
@resource_cluster_self_api.route('/<provider>/<cluster_name>')
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Fetch cloud resources from service account file',
            'schema': ResourceClusterSelfSchema
        }
    }
})
def fetchClusterDetail(provider, cluster_name):
    """
    Fetch cluster detail using cloud API's in real time.
    ---
    parameters:
      - name: provider
        in: path
        type: string
        enum: ['gcp', 'aws', 'azure']
        required: true
        default: aws
      - name: cluster_name
        type: string
        required: true
        in: path
    """
    pretty_resources = {}
    try:
        resource_service_obj = ResourceClusterSelfService(provider, cluster_name)
        pretty_resources = resource_service_obj.get_resource()
    except Exception as ex:
        exception = {
            "message": ex,
            "status": 400
        }
        return ExceptionSchema().dump(ExceptionModel(exception)), 400

    return ResourceClusterSelfSchema().dump(ResourceClusterSelfModel(pretty_resources)), 200

@resource_cluster_self_api.route('/<provider>/<cluster_name>', methods=['POST'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Update logging of the cluster',
            'schema': ResourceClusterSelfSchema
        }
    }
})
def updateCluster(provider, cluster_name):
    """
    Fetch cluster detail using cloud API's in real time.
    ---
    parameters:
      - name: provider
        in: path
        type: string
        enum: ['gcp', 'aws', 'azure']
        required: true
        default: aws
      - name: cluster_name
        type: string
        required: true
        in: path
      - name: body
        in: body
        schema: 
            type: object
            properties:
                clusterLogging:
                    type: string
        required: true
    """
    data = request.json
    pretty_resources = {}
    try:
        resource_service_obj = ResourceClusterSelfService(provider, cluster_name)
        pretty_resources = resource_service_obj.update_cluster_logging(data)
    except Exception as ex:
        exception = {
            "message": ex,
            "status": 400
        }
        return ExceptionSchema().dump(ExceptionModel(exception)), 400
    return ResourceClusterSelfSchema().dump(ResourceClusterSelfModel(pretty_resources)), 200
