import asyncio
import logging
import json
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse
from typing import List

from fastapi.middleware.cors import CORSMiddleware
from generate_svg import generate_svg, generate_tags
import random

app = FastAPI()

# Lista przechowująca adresy URL obrazków
images = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Zarządzanie połączeniami WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except WebSocketDisconnect:
                self.active_connections.remove(connection)
            except Exception as e:
                logging.error(f"Error occurred: {e}")
                self.active_connections.remove(connection)

manager = ConnectionManager()

# Strona HTML wyświetlająca obrazki
@app.get("/")
async def get():
    return HTMLResponse(html)

# Endpoint do dodawania obrazków
@app.post("/add_images/")
async def add_image(n: int):
    for i in range(n):
        index = len(images)
        tags = generate_tags()
        image = generate_svg()
        images.append({'id': index, 'tags': tags, 'svg': image})
    
    await manager.send_message(json.dumps({'number_of_images': n}))
    return {"message": "Image added"}

# Endpoint do pobierania obrazków
@app.get("/images/")
async def get_images():
    info = [{'id': image['id'], 'tags': image['tags']} for image in images]
    return info

@app.get("/image/{id}")
async def get_image(id: int):
    n = random.randint(0, 10)
    if n == 0:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    elif n == 1:
        await asyncio.sleep(random.randint(3, 10))
    return images[id]['svg']


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await asyncio.sleep(1)
            #await manager.broadcast(f"Client #{client_id} added: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        #await manager.broadcast(f"Client #{client_id} left the chat")


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Images</title>
    </head>
    <body>
        <h1>Images</h1>
        <div id="images"></div>
        <script>
            // Pobierz obrazki po załadowaniu strony
            fetch('/images/')
                .then(response => response.json())
                .then(data => {
                    const imagesDiv = document.getElementById('images');
                    data.images_urls.forEach(imageUrl => {
                        const img = document.createElement('img');
                        img.src = imageUrl;
                        imagesDiv.appendChild(img);
                    });
                });
        </script>
    </body>
</html>
"""
