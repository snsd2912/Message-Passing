import time
from concurrent import futures

import grpc
import location_pb2
import location_pb2_grpc
import os

from kafka import KafkaProducer

import logging
import json


KAFKA_SERVER = os.environ["KAFKA_SERVER"]
TOPIC_NAME = os.environ["TOPIC_NAME"]

logging.info('Connecting to Kafka Server...')
producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)
logging.info('Connected to Kafka Server at: {KAFKA_SERVER}')

class LocationServicer(locaton_pb2_grpc.LocationServiceServicer):
    def Create(self, request, context):

        request_value = {
            'person_id': int(request.person_id),
            'longitude': int(request.longitude),
            'latitude': int(request.latitude)
        }

        logging.info('Processing: {request_value}')

        send_data = json.dumps(request_value).encode('utf-8')

        producer.send(TOPIC_NAME, send_data)
        producer.flush()

        return location_pb2.LocationMessage(**request_value)

server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)

logging.info("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()

try:
    while True:
        time.sleep(86400)  # Sleep for 86400 seconds (1 day)
except KeyboardInterrupt:
    server.stop(0)
