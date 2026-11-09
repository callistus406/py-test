from fastapi  import FastAPI,WebSocket,WebSocketDisconnect
from fastapi.responses import HTMLResponse
app=FastAPI()




# 
@app.websocket("/ws")
async def new_connection(websocket:WebSocket):
    try:
        await  websocket.accept()
        while True:
            # recieve msg from the client
            msg =  await websocket.receive_text()

            await websocket.send_text("data recieved")

          
    except Exception as e:
        print(e)
