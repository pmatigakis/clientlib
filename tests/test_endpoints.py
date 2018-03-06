from unittest import TestCase, main
from unittest.mock import MagicMock
from collections import namedtuple

from marshmallow import post_load
from marshmallow.schema import Schema
from marshmallow.fields import Str

from clientlib.endpoints import Endpoint
from clientlib.models import Response, EndpointResponse
from clientlib.exceptions import ResponseDeserializationError, ExecutionError


SampleResponse = namedtuple("SampleResponse", ["message"])
SamplePayload = namedtuple("SamplePayload", ["message"])


class SampleResponseSchema(Schema):
    message = Str(required=True)

    @post_load
    def make_response(self, data):
        return SampleResponse(**data)


class SamplePayloadSchema(Schema):
    message = Str(required=True)

    @post_load
    def make_response(self, data):
        return SamplePayload(**data)


class EndpointTests(TestCase):
    def test_execute(self):
        function_mock = MagicMock()
        function_mock.execute.return_value = Response(
            status_code=200,
            headers={
                "Content-Type": "application/json"
            },
            json={
                "message": "hello world"
            }
        )

        endpoint = Endpoint(
            method="GET",
            endpoint="/test",
        )
        endpoint._function = function_mock

        response = endpoint.execute()

        self.assertIsInstance(response, Response)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.headers,
            {
                "Content-Type": "application/json"
            }
        )
        self.assertDictEqual(
            response.json,
            {
                "message": "hello world"
            }
        )

        function_mock.execute.assert_called_once_with(
            args={}, params={}, json=None)

    def test_execute_with_args(self):
        function_mock = MagicMock()
        function_mock.execute.return_value = Response(
            status_code=200,
            headers={
                "Content-Type": "application/json"
            },
            json={
                "message": "hello world"
            }
        )

        endpoint = Endpoint(
            method="GET",
            endpoint="/test/{arg1}",
            args=["arg1"]
        )
        endpoint._function = function_mock

        response = endpoint.execute(arg1="value")

        self.assertIsInstance(response, Response)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.headers,
            {
                "Content-Type": "application/json"
            }
        )
        self.assertDictEqual(
            response.json,
            {
                "message": "hello world"
            }
        )

        function_mock.execute.assert_called_once_with(
            args={
                "arg1": "value"
            },
            params={},
            json=None
        )

    def test_execute_with_params(self):
        function_mock = MagicMock()
        function_mock.execute.return_value = Response(
            status_code=200,
            headers={
                "Content-Type": "application/json"
            },
            json={
                "message": "hello world"
            }
        )

        endpoint = Endpoint(
            method="GET",
            endpoint="/test",
            params=["param1"]
        )
        endpoint._function = function_mock

        response = endpoint.execute(param1="value")

        self.assertIsInstance(response, Response)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.headers,
            {
                "Content-Type": "application/json"
            }
        )
        self.assertDictEqual(
            response.json,
            {
                "message": "hello world"
            }
        )

        function_mock.execute.assert_called_once_with(
            args={},
            params={
                "param1": "value"
            },
            json=None
        )

    def test_execute_with_response_schema(self):
        function_mock = MagicMock()
        function_mock.execute.return_value = Response(
            status_code=200,
            headers={
                "Content-Type": "application/json"
            },
            json={
                "message": "hello world"
            }
        )

        endpoint = Endpoint(
            method="GET",
            endpoint="/test",
            response_schema=SampleResponseSchema()
        )
        endpoint._function = function_mock

        response = endpoint.execute()

        self.assertIsInstance(response, EndpointResponse)
        self.assertIsInstance(response.response, Response)
        self.assertIsInstance(response.data, SampleResponse)
        self.assertEqual(response.response.status_code, 200)
        self.assertDictEqual(
            response.response.headers,
            {
                "Content-Type": "application/json"
            }
        )
        self.assertDictEqual(
            response.response.json,
            {
                "message": "hello world"
            }
        )
        self.assertEqual(response.data.message, "hello world")

        function_mock.execute.assert_called_once_with(
            args={}, params={}, json=None)

    def test_execute_with_response_schema_and_unsuccessful_status_code(self):
        function_mock = MagicMock()
        function_mock.execute.return_value = Response(
            status_code=404,
            headers={
                "Content-Type": "application/json"
            },
            json={
                "error": "operation failed"
            }
        )

        endpoint = Endpoint(
            method="GET",
            endpoint="/test",
            response_schema=SampleResponseSchema()
        )
        endpoint._function = function_mock

        with self.assertRaises(ExecutionError) as e:
            endpoint.execute()

        self.assertEqual(
            e.exception.reason, "the request was not executed successfully")
        self.assertEqual(e.exception.response.status_code, 404)
        self.assertDictEqual(
            e.exception.response.headers,
            {
                "Content-Type": "application/json"
            }
        )
        self.assertDictEqual(
            e.exception.response.json,
            {
                "error": "operation failed"
            }
        )

        function_mock.execute.assert_called_once_with(
            args={}, params={}, json=None)

    def test_execute_with_response_schema_and_invalid_response(self):
        function_mock = MagicMock()
        function_mock.execute.return_value = Response(
            status_code=200,
            headers={
                "Content-Type": "application/json"
            },
            json={
                "something": "this is not valid response data"
            }
        )

        endpoint = Endpoint(
            method="GET",
            endpoint="/test",
            response_schema=SampleResponseSchema()
        )
        endpoint._function = function_mock

        with self.assertRaises(ResponseDeserializationError) as e:
            endpoint.execute()

        self.assertIsInstance(e.exception, ResponseDeserializationError)
        self.assertEqual(
            e.exception.reason,
            "errors exist in deserialized endpoint response"
        )
        self.assertDictEqual(
            e.exception.errors,
            {
                "message": ["Missing data for required field."]
            }
        )
        self.assertEqual(e.exception.response.status_code, 200)
        self.assertDictEqual(
            e.exception.response.headers,
            {
                "Content-Type": "application/json"
            }
        )
        self.assertDictEqual(
            e.exception.response.json,
            {
                "something": "this is not valid response data"
            }
        )

        function_mock.execute.assert_called_once_with(
            args={}, params={}, json=None)

    def test_execute_with_strict_response_schema_and_invalid_response(self):
        function_mock = MagicMock()
        function_mock.execute.return_value = Response(
            status_code=200,
            headers={
                "Content-Type": "application/json"
            },
            json={
                "something": "this is not valid response data"
            }
        )

        endpoint = Endpoint(
            method="GET",
            endpoint="/test",
            response_schema=SampleResponseSchema(strict=True)
        )
        endpoint._function = function_mock

        with self.assertRaises(ResponseDeserializationError) as e:
            endpoint.execute()

        self.assertIsInstance(e.exception, ResponseDeserializationError)
        self.assertEqual(
            e.exception.reason,
            "failed to deserialize endpoint response"
        )
        self.assertDictEqual(
            e.exception.errors,
            {
                "message": ["Missing data for required field."]
            }
        )
        self.assertEqual(e.exception.response.status_code, 200)
        self.assertDictEqual(
            e.exception.response.headers,
            {
                "Content-Type": "application/json"
            }
        )
        self.assertDictEqual(
            e.exception.response.json,
            {
                "something": "this is not valid response data"
            }
        )

        function_mock.execute.assert_called_once_with(
            args={}, params={}, json=None)

    def test_execute_with_payload(self):
        function_mock = MagicMock()
        function_mock.execute.return_value = Response(
            status_code=200,
            headers={
                "Content-Type": "application/json"
            },
            json={
                "message": "hello world"
            }
        )

        endpoint = Endpoint(
            method="GET",
            endpoint="/test",
            payload_schema=SamplePayloadSchema(),
            payload="data"
        )
        endpoint._function = function_mock

        response = endpoint.execute(data={"message": "hello"})

        self.assertIsInstance(response, Response)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.headers,
            {
                "Content-Type": "application/json"
            }
        )
        self.assertDictEqual(
            response.json,
            {
                "message": "hello world"
            }
        )

        function_mock.execute.assert_called_once_with(
            args={},
            params={},
            json={
                "message": "hello"
            }
        )

    def test_execute_with_payload_schema(self):
        function_mock = MagicMock()
        function_mock.execute.return_value = Response(
            status_code=200,
            headers={
                "Content-Type": "application/json"
            },
            json={
                "message": "hello world"
            }
        )

        endpoint = Endpoint(
            method="GET",
            endpoint="/test",
            payload_schema=SamplePayloadSchema(),
            payload="data"
        )
        endpoint._function = function_mock

        response = endpoint.execute(data=SamplePayload(message="hello"))

        self.assertIsInstance(response, Response)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.headers,
            {
                "Content-Type": "application/json"
            }
        )
        self.assertDictEqual(
            response.json,
            {
                "message": "hello world"
            }
        )

        function_mock.execute.assert_called_once_with(
            args={},
            params={},
            json={
                "message": "hello"
            }
        )


if __name__ == "__main__":
    main()
