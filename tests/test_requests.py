from unittest import TestCase, main

import responses
from requests import Session
from requests.exceptions import RequestException, Timeout

from clientlib.requests import APIRequest
from clientlib.models import Response
from clientlib.exceptions import (
    InvalidResponseContentType, EndpointTimeout, EndpointRequestError
)


class APIRequestTests(TestCase):
    @responses.activate
    def test_execute(self):
        responses.add(
            responses.GET,
            "http://localhost/api/v1/test",
            json={
                "message": "hello world"
            },
            status=200
        )

        request = APIRequest(
            session=Session(),
            base_url="http://localhost",
            method="GET",
            endpoint="/api/v1/test"
        )

        api_response = request.execute()

        self.assertIsInstance(api_response, Response)
        self.assertEqual(api_response.status_code, 200)
        self.assertIn("Content-Type", api_response.headers)
        self.assertEqual(
            api_response.headers["Content-Type"], "application/json")
        self.assertDictEqual(
            api_response.json,
            {
                "message": "hello world"
            }
        )

    @responses.activate
    def test_execute_with_args(self):
        responses.add(
            responses.GET,
            "http://localhost/api/v1/test/1",
            json={
                "message": "hello world"
            },
            status=200
        )

        request = APIRequest(
            session=Session(),
            base_url="http://localhost",
            method="GET",
            endpoint="/api/v1/test/{arg1}",
            args={
                "arg1": 1
            }
        )

        api_response = request.execute()

        self.assertIsInstance(api_response, Response)
        self.assertEqual(api_response.status_code, 200)
        self.assertIn("Content-Type", api_response.headers)
        self.assertEqual(
            api_response.headers["Content-Type"], "application/json")
        self.assertDictEqual(
            api_response.json,
            {
                "message": "hello world"
            }
        )

    @responses.activate
    def test_fail_with_invalid_response_content_type(self):
        responses.add(
            responses.GET,
            "http://localhost/api/v1/test",
            body="hello world",
            status=200
        )

        request = APIRequest(
            session=Session(),
            base_url="http://localhost",
            method="GET",
            endpoint="/api/v1/test"
        )

        with self.assertRaises(InvalidResponseContentType) as e:
            request.execute()

        self.assertEqual(e.exception.status_code, 200)
        self.assertEqual(e.exception.content, "hello world")

    @responses.activate
    def test_timeout_exception_raised(self):
        responses.add(
            responses.GET,
            "http://localhost/api/v1/test",
            body=Timeout(),
        )

        request = APIRequest(
            session=Session(),
            base_url="http://localhost",
            method="GET",
            endpoint="/api/v1/test"
        )

        with self.assertRaises(EndpointTimeout) as e:
            request.execute()

        self.assertEqual(
            e.exception.reason, "a timeout occurred while executing request")
        self.assertEqual(e.exception.base_url, "http://localhost")
        self.assertEqual(e.exception.method, "GET")
        self.assertEqual(e.exception.endpoint, "/api/v1/test")

    @responses.activate
    def test_request_exception_raised(self):
        responses.add(
            responses.GET,
            "http://localhost/api/v1/test",
            body=RequestException(),
        )

        request = APIRequest(
            session=Session(),
            base_url="http://localhost",
            method="GET",
            endpoint="/api/v1/test"
        )

        with self.assertRaises(EndpointRequestError) as e:
            request.execute()

        self.assertEqual(
            e.exception.reason, "an error occurred while executing request")
        self.assertEqual(e.exception.base_url, "http://localhost")
        self.assertEqual(e.exception.method, "GET")
        self.assertEqual(e.exception.endpoint, "/api/v1/test")


if __name__ == "__main__":
    main()
