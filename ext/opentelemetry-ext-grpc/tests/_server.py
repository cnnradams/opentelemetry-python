# Copyright 2019 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from threading import Thread
from concurrent import futures

import grpc
from .protobuf import test_server_pb2, test_server_pb2_grpc

SERVER_ID = 1

class TestServer(test_server_pb2_grpc.GRPCTestServerServicer):

    def SimpleMethod(self, request, context):
        if request.request_data == "error":
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return test_server_pb2.Response()
        response = test_server_pb2.Response(
            server_id=SERVER_ID,
            response_data="Unary-Unary Response")
        return response

    def ClientStreamingMethod(self, request_iterator, context):
        data = list(request_iterator)
        if data[0].request_data == "error":
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return test_server_pb2.Response()
        response = test_server_pb2.Response(
            server_id=SERVER_ID,
            response_data="Stream-Unary Response")
        return response

    def ServerStreamingMethod(self, request, context):
        if request.request_data == "error":
            def err_gen():
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                yield test_server_pb2.Response()
            return err_gen()

        # create a generator
        def response_messages():
            for i in range(5):
                response = test_server_pb2.Response(
                    server_id=SERVER_ID,
                    response_data=("Unary-Stream Response message=%d" % i))
                yield response

        return response_messages()

    def BidirectionalStreamingMethod(self, request_iterator, context):
        data = list(request_iterator)
        if data[0].request_data == "error":
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            yield test_server_pb2.Response()
            return

        for i in range(5):
            yield test_server_pb2.Response(
                server_id=SERVER_ID,
                response_data=("send by Python server, message= %d" % i))

def create_test_server(port):
    server = grpc.server(futures.ThreadPoolExecutor())

    test_server_pb2_grpc.add_GRPCTestServerServicer_to_server(TestServer(), server)

    server.add_insecure_port(f"localhost:{port}")
    
    return server