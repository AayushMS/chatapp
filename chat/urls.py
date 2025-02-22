from django.urls import path

from chat import views

app_name = 'chat'

urlpatterns = [
    path('', views.home, name='home'),
    path('room/', views.room, name='room'),
    path('llm/chat/', views.llm_chat, name='llm_chat'),
]
