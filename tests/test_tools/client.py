import json

from flask.testing import FlaskClient
from werkzeug.wrappers import Response


class ApiResponse(Response):

    @property
    def json(self):
        return json.loads(self.data)


class ApiClient(FlaskClient):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.response_wrapper = ApiResponse
        self.api = ApiRequest(self)


class ApiRequest:

    def __init__(self, client: ApiClient):
        self.client = client

    def _api_call(self, method: str, expected: int, *args, **kwargs) -> dict:
        kwargs = self._prepate_kwargs(**kwargs)
        as_response = kwargs.pop('as_response', False)

        response = getattr(self.client, method)(*args, **kwargs)

        if as_response:
            return response

        assert response.status_code == expected, (
            f'Expected "{expected}", got "{response.status_code}"')

        try:
            return response.json
        except json.decoder.JSONDecodeError:
            return None

    def _prepate_kwargs(self, **kwargs) -> dict:
        data = kwargs.pop('data', None)
        kwargs['content_type'] = 'application/json'
        if data is not None:
            kwargs['data'] = json.dumps(data)
        return kwargs

    def get(self, *args, **kwargs) -> dict:
        return self._api_call('get', 200, *args, **kwargs)

    def post(self, *args, **kwargs) -> dict:
        return self._api_call('post', 201, *args, **kwargs)

    def put(self, *args, **kwargs) -> dict:
        return self._api_call('put', 200, *args, **kwargs)

    def delete(self, *args, **kwargs) -> dict:
        return self._api_call('delete', 204, *args, **kwargs)

    def options(self, *args, **kwargs) -> dict:
        return self._api_call('options', 200, *args, **kwargs)
