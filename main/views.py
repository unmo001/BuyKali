# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView

from main.forms import MessageForm
from registration.models import Message


class MessageRoomView(FormView):
    template_name = 'main/message_room.html'
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('main:message_room')

    def get_context_data(self, **kwargs):
        context = super(MessageRoomView, self).get_context_data(**kwargs)
        context['massages'] = Message.objects.all().order_by('published_at')
        return context






