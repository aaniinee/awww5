from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse
from typing import List, Dict

app = FastAPI()

# Lista przechowująca adresy URL obrazków
images = [
    {"id": 1, "url": "https://nrdc.org/sites/default/files/styles/huge_16x9_100/public/2023-04/talmie-peak-trail-wa-0pkjf1WRkU0.jpg.jpg?h=5ef39005&itok=_yOGQ1Xi", "tags": ["nature", "water"]},
    {"id": 2, "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/New_York_City_at_night_HDR.jpg/1024px-New_York_City_at_night_HDR.jpg", "tags": ["city", "night"]},
    {"id": 3, "url": "https://as2.ftcdn.net/v2/jpg/05/75/86/03/1000_F_575860305_xv2g4mWVLaM4rP8UBQcLLkXkUWu0jeJ9.jpg", "tags": ["nature", "forest"]},
    # dodaj więcej obrazków, jeśli chcesz
]

# Zarządzanie połączeniami WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# Strona HTML wyświetlająca obrazki
@app.get("/")
async def get():
    return HTMLResponse(html)

"""
# Endpoint do dodawania obrazków
@app.post("/add_image/")
async def add_image(image_url: str):
    images_urls.append(image_url)
    message = f"New image added: {image_url}"
    await manager.broadcast(message)
    return {"message": "Image added"}
"""
# Endpoint do pobierania obrazków
@app.get("/images", response_model=List[Dict])
async def get_images():
    return images

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
            fetch('/images')
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
