from channels.middleware import BaseMiddleware
from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model

class WebSocketAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # Add user to scope if not already present
        if "user" not in scope:
            scope["user"] = AnonymousUser()
        
        # Get headers dict
        headers = dict(scope['headers'])
        
        # Extract host
        if b'host' in headers:
            scope['server'] = headers[b'host'].decode('ascii').split(':')[0]

        return await super().__call__(scope, receive, send)