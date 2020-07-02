import threading
from concurrent import futures

import grpc
from ._client import simple_method, server_streaming_method, client_streaming_method, bidirectional_streaming_method
from ._server import create_test_server
from tests.protobuf import test_server_pb2_grpc
import opentelemetry.ext.grpc
from opentelemetry import trace
from opentelemetry.ext.grpc import client_interceptor
from opentelemetry.ext.grpc.grpcext import intercept_channel
from opentelemetry.sdk import trace as trace_sdk
from opentelemetry.test.test_base import TestBase

class TestClientProto(TestBase):
    def setUp(self):
        super().setUp()
        self.server = create_test_server(25565)
        self.server.start()
        
        interceptor = client_interceptor()
        self.channel = intercept_channel(grpc.insecure_channel("localhost:25565"), interceptor)
        self._stub = test_server_pb2_grpc.GRPCTestServerStub(self.channel)

    def tearDown(self):
        super().tearDown()
        self.server.stop(None)

    def test_unary_unary(self):
        simple_method(self._stub)
        spans = self.memory_exporter.get_finished_spans()
        self.assertEqual(len(spans), 1)
        span = spans[0]

        self.assertEqual(span.name, "/GRPCTestServer/SimpleMethod")
        self.assertIs(span.kind, trace.SpanKind.CLIENT)

        # Check version and name in span's instrumentation info
        self.check_span_instrumentation_info(span, opentelemetry.ext.grpc)

    def test_unary_stream(self):
        server_streaming_method(self._stub)
        spans = self.memory_exporter.get_finished_spans()
        self.assertEqual(len(spans), 1)
        span = spans[0]

        self.assertEqual(span.name, "/GRPCTestServer/ServerStreamingMethod")
        self.assertIs(span.kind, trace.SpanKind.CLIENT)

        # Check version and name in span's instrumentation info
        self.check_span_instrumentation_info(span, opentelemetry.ext.grpc)

    def test_stream_unary(self):
        client_streaming_method(self._stub)
        spans = self.memory_exporter.get_finished_spans()
        self.assertEqual(len(spans), 1)
        span = spans[0]

        self.assertEqual(span.name, "/GRPCTestServer/ClientStreamingMethod")
        self.assertIs(span.kind, trace.SpanKind.CLIENT)

        # Check version and name in span's instrumentation info
        self.check_span_instrumentation_info(span, opentelemetry.ext.grpc)

    def test_stream_stream(self):
        bidirectional_streaming_method(self._stub)
        spans = self.memory_exporter.get_finished_spans()
        self.assertEqual(len(spans), 1)
        span = spans[0]

        self.assertEqual(span.name, "/GRPCTestServer/BidirectionalStreamingMethod")
        self.assertIs(span.kind, trace.SpanKind.CLIENT)

        # Check version and name in span's instrumentation info
        self.check_span_instrumentation_info(span, opentelemetry.ext.grpc)
    
    def test_errors(self):
        with self.assertRaises(Exception):
            simple_method(self._stub, error=True)
        with self.assertRaises(Exception):
            server_streaming_method(self._stub, error=True)
        with self.assertRaises(Exception):
            client_streaming_method(self._stub, error=True)
        with self.assertRaises(Exception):
            bidirectional_streaming_method(self._stub, error=True)
        
        spans = self.memory_exporter.get_finished_spans()
        self.assertEqual(len(spans), 4)
        for span in spans:
            self.assertEqual(span.status.canonical_code, grpc.StatusCode.INVALID_ARGUMENT.value[0])
