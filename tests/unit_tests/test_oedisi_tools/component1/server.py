from oedisi.types.common import BrokerConfig
from component1 import TestFederate
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict
import uvicorn
import socket
import json
import sys

app = FastAPI()


@app.get("/")
def read_root():
    hostname = socket.gethostname()
    host_ip = socket.gethostbyname(hostname)
    return {"hostname": hostname, "host_ip": host_ip}


@app.post("/run/")
async def run_model(broker_config: BrokerConfig, background_tasks: BackgroundTasks):
    federate = TestFederate()
    try:
        background_tasks.add_task(federate.run)
        return {"reply": "success", "error": False}
    except Exception as e:
        return {"reply": str(e), "error": True}


if __name__ == "__main__":
    port = int(sys.argv[2])
    uvicorn.run(app, host="0.0.0.0", port=port)
