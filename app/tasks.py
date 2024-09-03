import os
from typing import Any
from .celery_app import celery_app
import random 

import time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


# def send_batch_data(ntime=5000):
#     points = []

#     for _ in range(ntime):
#         timestamp = time.time_ns()  # Capture the current time for all sensor values in this set
#         for sensor_id in range(1, 65):
#             sensor_name = f"s{sensor_id}"
#             value = random.uniform(20.0, 30.0)  # Random float between 20 and 30
#             point = (
#                 Point("sensor_data")
#                 .tag("sensor_id", sensor_name)
#                 .field("value", value)
#                 .time(timestamp, WritePrecision.NS)
#             )
#             points.append(point)
#             # time.sleep(0.5)

#     # Write all points in a single batch
#     write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=points)
#     print(f"Sent {len(points)} points to InfluxDB.")



# def send_single_point(ntime=5000):
#     points = []

#     for i in range(ntime):
#         timestamp = time.time_ns()  # Capture the current time for all sensor values in this set
#         for sensor_id in range(1, 65):
#             sensor_name = f"s{sensor_id}"
#             if 1000 < i <2000:     
#                 value = random.uniform(20.0, 30.0)  

#             else:
#                 value = random.uniform(0.0, 3.0)
            
#             point = (
#                 Point("sensor_data")
#                 .tag("sensor_id", sensor_name)
#                 .field("value", value)
#                 .time(timestamp, WritePrecision.NS)
#             )
#             write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)

#             points.append(point)
#             time.sleep(0.0005)

#     # Write all points in a single batch
#     #write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=points)
#     print(f"Sent {len(points)} points to InfluxDB.")



@celery_app.task(name="tasks.simulation")
def simulation(counter = 50000, BUCKET : Any = None):
    points = []

    # Configuration for InfluxDB
    INFLUXDB_URL = os.getenv("INFLUXDB_URL", "http://localhost:8086")  # Default to localhost for local development
    INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN", "your-influxdb-token")
    INFLUXDB_ORG = os.getenv("INFLUXDB_ORG", "your-org")
    if BUCKET is None:
        INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET", "your-bucket")
    else:
        INFLUXDB_BUCKET = BUCKET
    # Initialize InfluxDB client
    client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
    write_api = client.write_api(write_options=SYNCHRONOUS)

    for i in range(counter):
        timestamp = time.time_ns()  # Capture the current time for all sensor values in this set
        for sensor_id in range(1, 65):
            sensor_name = f"s{sensor_id}"
            if 1000 < i <2000:     
                value = random.uniform(20.0, 30.0)  

            else:
                value = random.uniform(0.0, 3.0)
            
            point = (
                Point("sensor_data")
                .tag("sensor_id", sensor_name)
                .field("value", value)
                .time(timestamp, WritePrecision.NS)
            )
            write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)

            points.append(point)
        time.sleep(0.0005)
    print(f"Sent {len(points)} points to InfluxDB.")
    return {"result" : 1}
