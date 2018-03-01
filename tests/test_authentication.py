from unittest import TestCase, main

from requests import Request

from clientlib.authentication import TokenAuthenticator


class TokenAuthenticatorTests(TestCase):
    def test_add_token_to_request(self):
        request = Request()

        authenticator = TokenAuthenticator("my-token")
        authenticator(request)

        self.assertDictEqual(
            request.headers,
            {
                "Authorization": "my-token"
            }
        )

    def test_add_token_with_type_to_request(self):
        request = Request()

        authenticator = TokenAuthenticator(
            token="my-token",
            authentication_type="Bearer"
        )
        authenticator(request)

        self.assertDictEqual(
            request.headers,
            {
                "Authorization": "Bearer my-token"
            }
        )


if __name__ == "__main__":
    main()
