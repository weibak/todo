import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from notes.forms import AddNoteForm, AuthForm, RegisterForm
from notes.models import Note


logger = logging.getLogger(__name__)


def index(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddNoteForm(request.POST)
            if form.is_valid():
                Note.objects.create(
                    author=request.user,
                    title=form.cleaned_data["title"],
                    text=form.cleaned_data["text"]
                )
                return redirect("index")
        else:
            form = AddNoteForm()
        notes = Note.objects.all()
        return render(request, "note_list.html", {"notes": notes, "form": form})
    else:
        messages.info(request, f"You don't logIn")
        return redirect('login')


def sign_in(request):
    if request.method == "POST":
        form = AuthForm(request.POST)
        if form.is_valid():
            logger.info(form.cleaned_data)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.info(request, f"You are now logged in as {username}")
                    return redirect('index')
                else:
                    return HttpResponse('Disabled account')
            else:
                messages.info(request, f"You don't logup!")
                return redirect('logup')
    else:
        form = AuthForm
    return render(request, "login.html", {"form": form})


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            logger.info(form.cleaned_data)
            user = User(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect("index")
    else:
        form = RegisterForm()
    return render(request, "logup.html", {"form": form})


def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    logger.info(f"Note with id = {note}, successfully deleted!")
    note.delete()
    return redirect('index')
