import json
import time
import ollama
import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse, StreamingHttpResponse


def home(request):
    return render(request, 'chat/home.html')

def room(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        if room_name:
            return render(request, 'chat/room.html', {
                'room_name': room_name,
                'username': request.POST.get('username', 'Anonymous')
            })
    return redirect('chat:home')

def llm_chat(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            body = json.loads(request.body)
            message = body.get('message')
            username = body.get('username', 'Anonymous')

            if message:
                # Stream the LLM response
                return StreamingHttpResponse(
                    stream_llm_response(message),
                    content_type="text/plain"
                )
            else:
                return JsonResponse({'error': 'Message is required'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
    
    return render(request, 'chat/llm_chat.html', {
        'room_name': 'Chat with LLM',
        'username': 'Anonymous'
    })


def stream_llm_response(prompt):

    client = ollama.Client(host="http://127.0.0.1:11434")
    model = 'llama3.2'
    stream = client.chat(
                model=model,
                messages=[{
                    "role": "user",
                    "content": prompt
                }], 
                stream=True)
    for chunk in stream:
        yield chunk['message']['content']  
        time.sleep(0.01)  
        