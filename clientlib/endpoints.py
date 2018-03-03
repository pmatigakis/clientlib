from clientlib.functions import Function


class Endpoint(object):
    def __init__(self, method, endpoint, args=None, params=None, payload=None,
                 requires_auth=True):
        self._method = method
        self._endpoint = endpoint
        self._args = args or []
        self._params = params or []
        self._payload = payload
        self._requires_auth = requires_auth

        self._function = None

    def _initialize_function(self, obj):
        self._function = Function(
            base_url=obj.base_url,
            method=self._method,
            endpoint=self._endpoint,
            auth=obj.auth if self._requires_auth else None,
            timeout=obj.timeout,
            verify=obj.verify
        )

    def __get__(self, obj, obj_type):
        if self._function is None:
            self._initialize_function(obj)

        return self.execute

    def _create_payload(self, kwargs):
        return kwargs[self._payload] if self._payload is not None else None

    def _create_args(self, kwargs):
        return {
            arg: kwargs[arg]
            for arg in self._args
        }

    def _create_params(self, kwargs):
        return {
            param: kwargs[param]
            for param in self._params
            if param in kwargs
        }

    def execute(self, **kwargs):
        args = self._create_args(kwargs)
        params = self._create_params(kwargs)
        payload = self._create_payload(kwargs)

        return self._function.execute(
            args=args,
            params=params,
            json=payload
        )
