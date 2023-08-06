# coding: utf-8
import json

from modernrpc.exceptions import RPCInternalError, RPCInvalidRequest, RPCException, RPCParseError

try:
    # Python 3
    from json.decoder import JSONDecodeError
except ImportError:
    # Python 2: json.loads will raise a ValueError when loading json
    JSONDecodeError = ValueError

from django.http.response import HttpResponse
from django.utils.module_loading import import_string

from modernrpc import modernrpc_settings

from modernrpc.handlers.base import RPCHandler

JSONRPC = '__json_rpc'


class JSONRPCHandler(RPCHandler):

    def __init__(self, entry_point):
        super(JSONRPCHandler, self).__init__(entry_point, JSONRPC)

    @staticmethod
    def valid_content_types():
        return [
            'application/json',
        ]

    def loads(self, data):
        try:
            return json.loads(data)
        except JSONDecodeError as e:
            raise RPCParseError(str(e))

    def dumps(self, obj):
        try:
            encoder = import_string(modernrpc_settings.JSONRPC_DEFAULT_ENCODER)
            return json.dumps(obj, cls=encoder)
        except Exception:
            raise RPCInternalError('Unable to serialize result as valid JSON')

    def handle(self, request):

        request_id = None

        try:
            encoding = request.encoding or 'utf-8'
            data = request.body.decode(encoding)
            body = self.loads(data)

            if not isinstance(body, dict):
                raise RPCParseError('Invalid request: the object must be a struct')

            if 'id' in body:
                request_id = body['id']
            else:
                raise RPCInvalidRequest('Missing parameter "id"')

            if 'jsonrpc' not in body:
                raise RPCInvalidRequest('Missing parameter "jsonrpc"')
            elif 'method' not in body:
                raise RPCInvalidRequest('Missing parameter "method"')
            elif 'params' not in body:
                raise RPCInvalidRequest('Missing parameter "params"')

            if body['jsonrpc'] != '2.0':
                raise RPCInvalidRequest('Invalid request. The attribute "jsonrpc" must contains "2.0"')

            result = self.call_method(body['method'], body['params'])

            return self.result_success(result, request_id)

        except RPCException as e:
            return self.result_error(e, request_id)
        except Exception as e:
            return self.result_error(RPCInternalError(str(e)), request_id)

    @staticmethod
    def json_http_response(data):
        response = HttpResponse(data)
        response['Content-Type'] = 'application/json'
        return response

    def result_success(self, data, request_id):
        result = {
            'id': request_id,
            'jsonrpc': '2.0',
            'result': data,
        }
        return self.json_http_response(self.dumps(result))

    def result_error(self, exception, request_id=None, additional_data=None):
        result = {
            'id': request_id,
            'jsonrpc': '2.0',
            'error': {
                'code': exception.code,
                'message': exception.message,
            }
        }

        if additional_data:
            result['error']['data'] = json.dumps(additional_data)

        return self.json_http_response(self.dumps(result))
