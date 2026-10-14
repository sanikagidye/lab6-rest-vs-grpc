#!/usr/bin/env python3

import grpc
import argparse
import random
import time
import base64

import lab6_pb2
import lab6_pb2_grpc


def doAdd(stub, debug=False):

    request = lab6_pb2.addMsg(
        a=5,
        b=10
    )

    response = stub.Add(request)

    if debug:
        print("Sum:", response.sum)


def doRawImage(stub, debug=False):

    img = open(
        'Flatirons_Winter_Sunrise_edit_2.jpg',
        'rb'
    ).read()

    request = lab6_pb2.rawImageMsg(
        img=img
    )

    response = stub.RawImage(request)

    if debug:
        print(
            "Width:",
            response.width,
            "Height:",
            response.height
        )


def doDotProduct(stub, debug=False):

    a = [random.random() for _ in range(100)]
    b = [random.random() for _ in range(100)]

    request = lab6_pb2.dotProductMsg(
        a=a,
        b=b
    )

    response = stub.DotProduct(request)

    if debug:
        print(
            "Dot product:",
            response.dotproduct
        )


def doJsonImage(stub, debug=False):

    img = open(
        'Flatirons_Winter_Sunrise_edit_2.jpg',
        'rb'
    ).read()

    encoded = base64.b64encode(
        img
    ).decode('utf-8')

    request = lab6_pb2.jsonImageMsg(
        img=encoded
    )

    response = stub.JsonImage(request)

    if debug:
        print(
            "Width:",
            response.width,
            "Height:",
            response.height
        )


parser = argparse.ArgumentParser(
    description='gRPC client'
)

parser.add_argument(
    'host',
    help='Server hostname or IP'
)

parser.add_argument(
    'cmd',
    choices=[
        'add',
        'rawImage',
        'dotProduct',
        'jsonImage'
    ]
)

parser.add_argument(
    'reps',
    type=int
)

parser.add_argument(
    '-p',
    '--port',
    type=int,
    default=50051
)

parser.add_argument(
    '-d',
    '--debug',
    action='store_true'
)

args = parser.parse_args()


addr = f"{args.host}:{args.port}"

print(
    f"Running {args.reps} reps against {addr}"
)


channel = grpc.insecure_channel(addr)

stub = lab6_pb2_grpc.Lab6Stub(channel)


operations = {
    'add': doAdd,
    'rawImage': doRawImage,
    'dotProduct': doDotProduct,
    'jsonImage': doJsonImage
}


operation = operations[args.cmd]


start = time.perf_counter()

for _ in range(args.reps):
    operation(
        stub,
        debug=args.debug
    )

delta = (
    (time.perf_counter() - start)
    / args.reps
) * 1000


print(
    "Took",
    delta,
    "ms per operation"
)