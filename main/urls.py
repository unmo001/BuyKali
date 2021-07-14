from django.urls import path

from main import views

app_name = 'main'

urlpatterns = [
    path('message_room/',views.MessageRoomView.as_view(),name="message_room")
]