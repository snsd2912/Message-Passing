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
USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]

logging.info('Connecting to Kafka Server...')
# producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)
producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,  
    security_protocol='SASL_PLAINTEXT',    
    sasl_mechanism='SCRAM-SHA-256',                
    sasl_plain_username=USERNAME,
    sasl_plain_password=PASSWORD 
)
logging.info('Connected to Kafka Server at: {KAFKA_SERVER}')

class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    def Create(self, request, context):

        request_value = {
            'person_id': int(request.person_id),
            'latitude': int(request.latitude),
            'longitude': int(request.longitude)
        }

        logging.info('Processing: {request_value}')

        send_data = json.dumps(request_value, indent=2).encode('utf-8')

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
