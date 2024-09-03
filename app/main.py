import os
import random
import time
from typing import Union
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import time
import influxdb_client

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

from celery.result import AsyncResult
from .celery_app import celery_app

# Read InfluxDB configuration from environment variables
influxdb_url = os.getenv("INFLUXDB_URL", "http://localhost:8086")  # Default to localhost for local development
influxdb_token = os.getenv("INFLUXDB_TOKEN", "your-influxdb-token")
influxdb_org = os.getenv("INFLUXDB_ORG", "your-org")
influxdb_bucket = os.getenv("INFLUXDB_BUCKET", "your-bucket")

# Initialize the InfluxDB client
client = influxdb_client.InfluxDBClient(url=influxdb_url, token=influxdb_token, org=influxdb_org)
write_api = client.write_api(write_options=SYNCHRONOUS)

app = FastAPI()

class SensorData(BaseModel):
    sensor_id: str
    temperature: float
    humidity: float

@app.post("/simulateSinglePoint")
async def write_data(BUCKET: Union[str, None] = None ):
    try:
        counter = 1
        # for i in range(counter):
        timestamp = time.time_ns()  # Capture the current time for all sensor values in this set
        for sensor_id in range(1, 65):
            sensor_name = f"s{sensor_id}"
            value = random.uniform(0.0, 3.0)
            
            point = (
                Point("sensor_data")
                .tag("sensor_id", sensor_name)
                .field("value", value)
                .time(timestamp, WritePrecision.NS)
            )
            if BUCKET is not None:
                influxdb_bucket = BUCKET
            write_api.write(bucket=influxdb_bucket, org=influxdb_org, record=point)
        time.sleep(10)
        return {"message": "Data written successfully to InfluxDB"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/simulate/{nsteps}/{BUCKET}")
def simulate(nsteps: int, BUCKET: str = None):
    task = celery_app.send_task("tasks.simulation", args=[nsteps, BUCKET])
    return {"task_id": task.id}

@app.get("/result/{task_id}")
def get_result(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    if task_result.ready():
        return {"status": task_result.status, "result": task_result.result}
    else:
        return {"status": task_result.status, "result": None}
