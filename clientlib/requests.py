from requests import Session, Request

from clientlib.models import Response


class APIRequest(object):
    def __init__(self, base_url, method, endpoint, args=None, params=None,
                 json=None, auth=None, timeout=5, verify=True):
        self.base_url = base_url
        self.method = method
        self.endpoint = endpoint
        self.args = args
        self.params = params
        self.json = json
        self.auth = auth
        self.timeout = timeout
        self.verify = verify

    def _create_endpoint(self):
        if self.args is None:
            return self.endpoint
        else:
            return self.endpoint.format(**self.args)

    def _create_url(self):
        return "{base_url}{endpoint}".format(
            base_url=self.base_url,
            endpoint=self._create_endpoint()
        )

    def _create_session(self):
        return Session()

    def _create_request(self):
        return Request(
            method=self.method,
            url=self._create_url(),
            params=self.params,
            json=self.json,
            auth=self.auth
        )

    def execute(self):
        request = self._create_request()
        prepared_request = request.prepare()

        with self._create_session() as session:
            response = session.send(
                request=prepared_request,
                verify=self.verify,
                timeout=self.timeout
            )

        return Response(
            status_code=response.status_code,
            headers=response.headers,
            json=response.json()
        )
