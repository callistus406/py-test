
from fastapi import WebSocket


class  ConnectionManager:
    def __init__(self):
        # this is where we will store all active connections
        self.active_conn = {}

    async def connect(self,websocket:WebSocket,user_id):

        await websocket.accept()
        # store user and socket id
        self.active_conn[websocket] = user_id
        print(user_id+" connected to socket")

    async def disconnect(self,websocket:WebSocket):

        user_id = self.active_conn.pop(websocket)

        print(user_id, "disconnected")



manager = ConnectionManager()





