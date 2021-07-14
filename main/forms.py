from django import forms

from registration.models import Message


class MessageForm(forms.Form):
    class Meta:
        model = Message
        fields = ('message',)
