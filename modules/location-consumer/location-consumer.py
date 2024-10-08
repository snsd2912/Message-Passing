import json
import os

from kafka import KafkaConsumer
from sqlalchemy import create_engine

KAFKA_SERVER = os.environ["KAFKA_SERVER"]
TOPIC_NAME = os.environ["TOPIC_NAME"]

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]
USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]

logging.info('Connecting to Kafka Server...')
consumer = KafkaConsumer(
    TOPIC_NAME, 
    bootstrap_servers=[KAFKA_SERVER],
    security_protocol='SASL_PLAINTEXT',    
    sasl_mechanism='SCRAM-SHA-256',                
    sasl_plain_username=USERNAME,
    sasl_plain_password=PASSWORD 
)
print('Start listening topic: ' + TOPIC_NAME)

def connect_db():
    engine = create_engine(f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}", echo=True)
    return engine.connect()

def consume_and_save():
    connection = connect_db()
    try:
        print("Kafka consumer started with persistent DB connection...")

        for message in consumer:
            data = message.value.decode('utf-8')
            location = json.loads(data)
            person_id = int(location["person_id"])
            longitude, latitude = int(location["longitude"]), int(location["latitude"])

            insert = "INSERT INTO location (person_id, coordinate) VALUES ({}, ST_Point({}, {}))".format(person_id, latitude, longitude)

            print(insert)
            connection.execute(insert)

    except KeyboardInterrupt:
        print("Consumer interrupted, shutting down...")
    finally:
        connection.close()

consume_and_save()
