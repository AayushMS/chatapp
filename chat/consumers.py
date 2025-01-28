import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.info(f"WebSocket connect attempt from {self.scope.get('client', 'unknown')}")
        logger.info(f"Path: {self.scope['path']}")
        
        try:
            # Get room name from URL route
            self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
            self.room_group_name = f"chat_{self.room_name}"
            
            # Join room group first
            try:
                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )
                logger.info(f"Joined room group: {self.room_group_name}")
            except Exception as group_error:
                logger.error(f"Error joining room group: {str(group_error)}")
                return
            
            # Then accept the connection
            await self.accept()
            logger.info("WebSocket connection accepted")
            
        except Exception as e:
            logger.error(f"Error in connect: {str(e)}")
            # Don't raise the error, just close the connection
            await self.close()
            return

    async def disconnect(self, close_code):
        try:
            # Leave room group
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            logger.info(f"Disconnected from room {self.room_group_name}")
        except Exception as e:
            logger.error(f"Error in disconnect: {str(e)}")

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json["message"]

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "username": text_data_json["username"],
                }
            )
            logger.info(f"Message sent to room {self.room_group_name}")
        except Exception as e:
            logger.error(f"Error in receive: {str(e)}")

    async def chat_message(self, event):
        try:
            message = event["message"]
            username = event["username"]
            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                "message": message,
                "username": username
            }))
            logger.info(f"Message delivered to client: {username}")
        except Exception as e:
            logger.error(f"Error in chat_message: {str(e)}")