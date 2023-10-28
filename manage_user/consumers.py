import cv2
from django.shortcuts import render
import os
import csv
import time
import base64
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
import asyncio
class VideoStreamConsumer(AsyncWebsocketConsumer):
    cap = None
    async def connect(self):
        self.loop = asyncio.get_running_loop()
        print("Connecting")
        await self.accept()
        if not VideoStreamConsumer.cap:
            VideoStreamConsumer.cap = cv2.VideoCapture("https://firebasestorage.googleapis.com/v0/b/orderfood-5a6b6.appspot.com/o/highway.mp4?alt=media&token=267712b6-6b1f-47e8-9893-aa3b6e4c9dba&_gl=1*1316xqm*_ga*MjkzMTI0NDY1LjE2OTU3OTY4MzY.*_ga_CW55HF8NVT*MTY5Nzg2ODU0NC4yNS4x.LjE2OTc4Njg5MTAuMjEuMC4w")
            while VideoStreamConsumer.cap.isOpened():
                ret, frame = VideoStreamConsumer.cap.read()
                if not ret:
                    break
                print('Running ... connection')
                ret, buffer = cv2.imencode('.jpeg', frame)
                b64_img = base64.b64encode(buffer).decode('utf-8')
                await self.send(b64_img)
                await asyncio.sleep(0.1)

    async def disconnect(self, close_code):
        print(f"DISCONNECT WebSocket closed with code {close_code}.")
        if VideoStreamConsumer.cap:
            VideoStreamConsumer.cap.release()
            VideoStreamConsumer.cap = None
 