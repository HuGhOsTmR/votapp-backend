from fastapi import WebSocket


class ConnectionManager:

    def __init__(self):
        # { assembly_id: { user_id: { ws, user } } }
        self.active_connections = {}

    # 🔥 conectar usuario
    async def connect(self, assembly_id: str, websocket: WebSocket, user):

        await websocket.accept()

        if assembly_id not in self.active_connections:
            self.active_connections[assembly_id] = {}

        self.active_connections[assembly_id][str(user.id)] = {
            "ws": websocket,
            "user": user
        }

    # 🔥 desconectar usuario
    def disconnect(self, assembly_id: str, websocket: WebSocket):

        if assembly_id not in self.active_connections:
            return

        for user_id, conn in list(self.active_connections[assembly_id].items()):
            if conn["ws"] == websocket:
                del self.active_connections[assembly_id][user_id]

        # limpiar si ya no hay nadie
        if not self.active_connections[assembly_id]:
            del self.active_connections[assembly_id]

    # 🔥 broadcast seguro
    async def broadcast(self, assembly_id: str, message: dict):

        if assembly_id not in self.active_connections:
            return

        disconnected = []

        for user_id, conn in self.active_connections[assembly_id].items():
            try:
                await conn["ws"].send_json(message)
            except:
                disconnected.append(user_id)

        # limpiar conexiones muertas
        for user_id in disconnected:
            del self.active_connections[assembly_id][user_id]

    # 🔥 usuarios conectados
    def get_users(self, assembly_id: str):

        if assembly_id not in self.active_connections:
            return []

        return [
            {
                "id": user_id,
                "name": conn["user"].full_name,
                "party": conn["user"].party  # 🔥 NUEVO
            }
            for user_id, conn in self.active_connections[assembly_id].items()
        ]

    # 🔥 cantidad de usuarios
    def get_count(self, assembly_id: str):

        if assembly_id not in self.active_connections:
            return 0

        return len(self.active_connections[assembly_id])

    def get_quorum(self, assembly_id: str):

        connected = self.get_count(assembly_id)

        
        required = 2

        return {
            "connected": connected,
            "required": required,
            "has_quorum": connected >= required
        }