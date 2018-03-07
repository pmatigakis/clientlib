from clientlib.requests import APIRequest


class Function(object):
    def __init__(self, session, base_url, method, endpoint, auth=None,
                 timeout=5, verify=True):
        self.session = session
        self.base_url = base_url
        self.method = method
        self.endpoint = endpoint
        self.auth = auth
        self.timeout = timeout
        self.verify = verify

    def execute(self, args=None, params=None, json=None):
        request = APIRequest(
            session=self.session,
            base_url=self.base_url,
            method=self.method,
            endpoint=self.endpoint,
            args=args,
            params=params,
            json=json,
            auth=self.auth,
            timeout=self.timeout,
            verify=self.verify
        )

        return request.execute()
