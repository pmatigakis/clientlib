class Client(object):
    def __init__(self, base_url, auth=None, timeout=5, verify=True):
        self.base_url = base_url
        self.auth = auth
        self.timeout = timeout
        self.verify = verify
