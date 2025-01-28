from django.shortcuts import render, redirect

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