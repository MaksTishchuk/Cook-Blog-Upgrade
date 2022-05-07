from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import timedelta
from django.db.models.functions import Now

from .models import Message


@login_required
def chat(request):
    username = request.user.username
    messages = Message.objects.filter(room='all_users', date_added__gte=Now()-timedelta(hours=24))
    return render(
        request,
        'chat/room.html',
        {'room_name': 'all_users', 'username': username, 'messages': messages}
    )
