# serial_app.py
import asyncio
from typing import Optional

import serial_asyncio
from fastapi import FastAPI
import json

app = FastAPI()
now_serial_data = None

async def read_serial():
    global now_serial_data
    reader, _ = await serial_asyncio.open_serial_connection(
        url="/dev/pts/7", baudrate=9600
    )
    while True:
        try:
            line = await reader.readline()
            decoded = json.loads(line)
            print(f"[Serial] {decoded["sugar"]}")
            now_serial_data = decoded
        except Exception as e:
            print(f"[Error] {e}")
            await asyncio.sleep(1)

@app.on_event("startup")
async def start_serial_reader():
    asyncio.create_task(read_serial())

@app.get("/stock")
async def get_serial_data(type: Optional[str] = None):
    try:
        if type:
            return {type: now_serial_data[type]}
        return now_serial_data
    except Exception as e:
        return {"error": e}
