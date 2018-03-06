from unittest import TestCase, main

import responses

from clientlib.requests import APIRequest
from clientlib.models import Response


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


if __name__ == "__main__":
    main()
