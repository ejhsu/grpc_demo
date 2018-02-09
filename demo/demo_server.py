from concurrent import futures
import time

import grpc

import demo_pb2
import demo_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class DemoServicer(demo_pb2_grpc.DemoServicer):

  def HelloOnce(self, request, context):
    return demo_pb2.HelloResponse(message='Received your message: {}'.format(request.message))

  def LotsOfReplies(self, request, context):
    for c in request.message:
      time.sleep(1)
      yield demo_pb2.HelloResponse(message=c)

  def LotsOfHello(self, request_iterator, context):
    reply = ''
    for request in request_iterator:
      reply += request.message
    return demo_pb2.HelloResponse(message='Received your message: {}'.format(reply))

  def RepeatBot(self, request_iterator, context):
    received_message = ''
    for request in request_iterator:
      received_message += request.message
      yield demo_pb2.HelloResponse(message='Received your message: {}'.format(request.message))

    yield demo_pb2.HelloResponse(message='total length: {}'.format(len(received_message)))


def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  demo_pb2_grpc.add_DemoServicer_to_server(DemoServicer(), server)
  server.add_insecure_port('localhost:50051')
  server.start()
  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)


if __name__ == '__main__':
  serve()
