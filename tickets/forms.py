from django import forms
from .models import Ticket,Comment

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'desc', 'priority', 'assigned_to','status']
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {'content': 'Add a Comment'}