import time

import grpc

import demo_pb2
import demo_pb2_grpc


def run():
  channel = grpc.insecure_channel('localhost:50051')
  stub = demo_pb2_grpc.DemoStub(channel)
  return stub

def helloOnce(stub):
  response = stub.HelloOnce(demo_pb2.HelloRequest(message='Hello, world!'))
  print('Response message from server: {}'.format(response.message))

def lotsOfReplies(stub):
  response_iterator = stub.LotsOfReplies(demo_pb2.HelloRequest(message='Hello, world!'))
  for response in response_iterator:
    print('Response message from server: {}'.format(response.message))

def lotsOfHello(stub):
  response = stub.LotsOfHello(generate_messages())
  print('Response message from server: {}'.format(response.message))
  
def repeatBot(stub):
  # bi-directional streaming
  response_iterator = stub.RepeatBot(generate_messages())
  for response in response_iterator:
    print('Response message from server: {}'.format(response.message))


def generate_messages():
  messages = [demo_pb2.HelloRequest(message=c) for c in 'hello, world!']
  for msg in messages:
    print("Sending %s" % (msg.message))
    yield msg
    time.sleep(0.5)

if __name__ == '__main__':
  stub = run()
