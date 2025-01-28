// WebSocket Debug Helper
window.wsDebug = {
    checkConnection: function() {
        const ws = new WebSocket((window.location.protocol === 'https:' ? 'wss://' : 'ws://') + 
                               window.location.host + '/ws/chat/test/');
        
        ws.onopen = function() {
            console.log('Debug: WebSocket connection test successful');
            ws.close();
        };
        
        ws.onerror = function(e) {
            console.error('Debug: WebSocket connection test failed');
            console.log('Debug: Check if Django server is running with runserver');
            console.log('Debug: Check if Redis is running');
            console.log('Debug: Check browser console for additional errors');
        };
    }
};