# serial_app.py
import asyncio
from typing import Optional
import serial_asyncio
from fastapi import FastAPI
import json

from model import Order
from config import SERIAL_PORT, BAUDRATE
app = FastAPI()
now_serial_data = None
serial_task = None  # Task 핸들 저장

async def read_serial():
    global now_serial_data
    reader, _ = await serial_asyncio.open_serial_connection(
        url=SERIAL_PORT, baudrate=BAUDRATE
    )
    while True:
        try:
            line = await reader.readline()
            decoded = json.loads(line)
            print(f"[Serial] {decoded}")
            now_serial_data = decoded
        except Exception as e:
            print(f"[Error] {e}")
            await asyncio.sleep(1)

@app.on_event("startup")
async def start_serial_reader():
    global serial_task
    serial_task = asyncio.create_task(read_serial())

@app.on_event("shutdown")
async def stop_serial_reader():
    global serial_task
    if serial_task:
        serial_task.cancel()
        try:
            await serial_task
        except asyncio.CancelledError:
            print("[Shutdown] Serial reader cancelled cleanly.")
@app.get("/stock")
async def get_serial_data(type: Optional[str] = None):
    try:
        if type:
            return {type: now_serial_data[type]}
        return now_serial_data
    except Exception as e:
        return {"error": e}

@app.post("/order")
async def create_order(order: Order):
    if order:
        print(f"[Order Received] {order}")
        return {"status": "success"}
    return {"status": "error"}
