## WebSocket Connection Troubleshooting

If you're experiencing WebSocket connection issues, please ensure:

1. Redis server is running on your system:
```bash
redis-cli ping
```
Should return "PONG". If not, start Redis:
```bash
sudo service redis-server start  # On Ubuntu/Debian
brew services start redis       # On MacOS
```

2. Your Django Channels setup is correct (already verified in settings.py)
3. The development server is running with Channels/ASGI support:
```bash
python manage.py runserver
```

4. No firewall is blocking WebSocket connections on port 8000

5. You're accessing the chat through the correct URL pattern: http://127.0.0.1:8000/chat/[room-name]/

6. Check if Redis is working:
   ```python
   # Start Python shell
   python manage.py shell

   # Test Redis connection
   from channels.layers import get_channel_layer
   channel_layer = get_channel_layer()
   async def test_redis():
       await channel_layer.send("test", {"type": "test.message"})
   
   # Run the test (should not raise any errors)
   import asyncio
   asyncio.run(test_redis())
   ```

6. Open your browser's developer tools (F12) and check the Console tab for detailed error messages.

7. Try running the WebSocket connection test in your browser's console:
```javascript
wsDebug.checkConnection();
```

8. Make sure your Django development server is running with Daphne:
```bash
# Install daphne if not already installed
pip install daphne

# Start the server with the provided script
chmod +x run_server.sh
./run_server.sh

# Or manually with Python
python start_server.py
```

9. Check Redis is installed and running:
```bash
# Install Redis if needed
sudo apt-get install redis-server  # Ubuntu/Debian
brew install redis                # MacOS

# Start Redis
sudo service redis-server start   # Ubuntu/Debian
brew services start redis        # MacOS

# Verify Redis is running and accessible
redis-cli ping                   # Should return PONG
```

10. If still having issues, try these steps:
    - Clear your browser cache and reload
    - Check if Redis is running on the default port (6379)
    - Ensure no firewall is blocking WebSocket connections
    - Verify the ASGI application is properly configured
    - Check for any error messages in the Django/Daphne console