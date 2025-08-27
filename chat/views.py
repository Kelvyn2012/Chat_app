from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Message


def home(request):
    rooms = Room.objects.all()
    return render(request, "chat/home.html", {"rooms": rooms})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "chat/register.html", {"form": form})


@login_required
def room(request, room_name):
    room = Room.objects.get(slug=room_name)
    messages = Message.objects.filter(room=room).order_by("date_added")[:50]
    return render(
        request,
        "chat/room.html",
        {"room": room, "messages": messages, "user": request.user},
    )
