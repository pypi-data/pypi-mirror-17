import json
import requests
from inflection import underscore
from uritemplate import expand

from zc_common.jwt_auth.utils import service_jwt_payload_handler, jwt_encode_handler
from zc_common.settings import zc_settings


# Requests that can be made to another service
GET = 'get'
POST = 'post'
PUT = 'put'
PATCH = 'patch'


class UnsupportedHTTPMethodException(Exception):
    pass


class RouteNotFoundException(Exception):
    pass


class ServiceRequestException(Exception):
    """An exception commonly thrown when an HTTP request to another service endpoint fails."""
    message = None
    response = None

    def __init__(self, message, response):
        super(ServiceRequestException, self).__init__(message)
        self.message = message
        self.response = response


class RemoteResourceException(Exception):
    pass


class RemoteResourceWrapper(object):

    def __init__(self, data):
        self.data = data
        self.create_properties_from_data()

    def create_properties_from_data(self):
        accepted_keys = ('id', 'type', 'self', 'related')

        for key in self.data.keys():
            if key in accepted_keys:
                setattr(self, key, self.data.get(key))

        if 'attributes' in self.data:
            attributes = self.data['attributes']
            for key in attributes.keys():
                setattr(self, underscore(key), attributes[key])

        if 'relationships' in self.data:
            relationships = self.data['relationships']

            for key in relationships.keys():
                if isinstance(relationships[key]['data'], list):
                    setattr(self, underscore(key), RemoteResourceListWrapper(relationships[key]['data']))
                else:
                    setattr(self, underscore(key), RemoteResourceWrapper(relationships[key]['data']))

                if 'links' in relationships[key]:
                    setattr(getattr(self, underscore(key)), 'links',
                            RemoteResourceWrapper(relationships[key]['links']))


class RemoteResourceListWrapper(list):

    def __init__(self, seq):
        super(RemoteResourceListWrapper, self).__init__()
        self.data = seq
        self.add_items_from_data()

    def add_items_from_data(self):
        map(lambda x: self.append(RemoteResourceWrapper(x)), self.data)


def get_route_from_fk(resource_type, pk=None):
    """Gets a fully qualified URL for a given resource_type, pk"""
    routes = requests.get(zc_settings.GATEWAY_ROOT_PATH).json()

    for route in routes.iterkeys():
        if 'resource_type' in routes[route] and routes[route]['resource_type'] == resource_type:
            if isinstance(pk, (list, set)):
                expanded = '{}?filter[id__in]={}'.format(expand(route, {}), ','.join([str(x) for x in pk]))
            else:
                expanded = expand(route, {'id': pk})
            return '{0}{1}'.format(routes[route]['domain'], expanded)

    raise RouteNotFoundException('No route for resource_type: "{0}"'.format(resource_type))


def make_service_request(service_name, endpoint, method=GET, data=None):
    """
    Makes a JWT token-authenticated service request to the URL provided.

    Args:
        service_name: name of the service making this request. e.g. mp-users
        endpoint: the url to use
        method: HTTP method. supported methods are defined at this module's global variables
        data: request payload in case we are making a POST request

    Returns: text content of the response
    """

    jwt_token = jwt_encode_handler(service_jwt_payload_handler(service_name))
    headers = {'Authorization': 'JWT {}'.format(jwt_token), 'Content-Type': 'application/vnd.api+json'}

    if method not in [GET, POST, PUT, PATCH]:
        raise UnsupportedHTTPMethodException(
            "Method {0} is not supported. service_name: {1}, endpoint: {2}".format(method, service_name, endpoint))

    response = getattr(requests, method)(endpoint, headers=headers, json=data)

    if 400 <= response.status_code < 600:
        http_error_msg = '{0} Error: {1} for {2}. Content: {3}'.format(
            response.status_code, response.reason, response.url, response.text)
        raise ServiceRequestException(http_error_msg, response)

    return response


def wrap_resource_from_response(response):
    json_response = json.loads(response.text)

    if 'data' not in json_response:
        msg = 'Error retrieving resource. Url: {0}. Content: {1}'.format(response.request.url, response.content)
        raise RemoteResourceException(msg)

    resource_data = json_response['data']
    if isinstance(resource_data, list):
        return RemoteResourceListWrapper(resource_data)
    return RemoteResourceWrapper(resource_data)


def get_remote_resource(service_name, resource_type, pk):
    """A shortcut function to make a GET request to a remote service."""
    url = get_route_from_fk(resource_type, pk)
    response = make_service_request(service_name, url)
    wrapped_resource = wrap_resource_from_response(response)
    return wrapped_resource


def get_remote_resource_from_url(service_name, url):
    response = make_service_request(service_name, url)
    wrapped_resource = wrap_resource_from_response(response)
    return wrapped_resource
