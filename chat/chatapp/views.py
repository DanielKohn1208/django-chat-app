from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm, FriendForm
from .models import Message, Friend
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.core.serializers import serialize


@login_required
def unexpectedDisconnect(request):
    messages.error(request, "Unexpected Error Occured")
    return redirect('/chat')


@login_required
def unfriend(request):
    if request.method == "POST":
        roomName = request.POST['roomName']
        friendsToDelete = Friend.objects.filter(roomName=roomName)
        if len(friendsToDelete.filter(user=request.user)) == 0:
            messages.error(request, "Friend could not be deleted")
        else:
            friendsToDelete.delete()
            messages.success(request, "Friend was successfully unfriended")
        return redirect('/add-friend')


@login_required
def oldMessages(request, page, roomName):
    currentChat = Friend.objects.filter(roomName=roomName)[0]
    previousMessages = list(Message.objects.filter(
        friend1=currentChat).order_by('-dateSent')[page * 10:(page + 1) * 10])
    jsonData = serialize(
        "json",
        previousMessages,
        fields=(
            'sender',
            'receiver',
            'content'))
    return HttpResponse(jsonData, content_type="application/json")


@login_required
def chat(request, id=None):
    friends = Friend.objects.filter(user=request.user)
    if id is None:
        return render(request,
                      "chatapp/chat.html",
                      {'friends': friends,
                       "activeChatId": None,
                       "currentChat": None,
                       "previousMessage": None})
    try:
        currentChat = friends.get(friend=id)
    except ObjectDoesNotExist:
        messages.error(request, "Friend could not be found")
        return redirect("/chat")
    if currentChat.isUnread:
        currentChat.isUnread = False
        currentChat.save()
    previousMessages = reversed(list(Message.objects.filter(
        friend1=currentChat).order_by('-dateSent')[:10]))
    return render(request,
                  "chatapp/chat.html",
                  {'friends': friends,
                   "activeChatId": currentChat.roomName,
                   "currentChat": currentChat,
                   "previousMessages": previousMessages})


@login_required
def addFriend(request):
    if request.method == 'GET':
        f = FriendForm()
    elif request.method == 'POST':
        f = FriendForm(request.POST)
        if f.is_valid():
            name = f.cleaned_data.get('friendName')
            try:
                addFriend = User.objects.get(username=name)
                roomName = f"{request.user.username}-{addFriend.username}"
                newFriendrow1 = Friend(
                    user=request.user,
                    friend=addFriend,
                    roomName=roomName,
                    isUnread=False)
                newFriendrow2 = Friend(
                    user=addFriend,
                    friend=request.user,
                    roomName=roomName,
                    isUnread=False)
                newFriendrow1.save()
                newFriendrow2.save()
                messages.success(request, 'New Friend added')
            except ObjectDoesNotExist:
                messages.error(
                    request, 'The friend you were trying to add no longer exists')

            except IntegrityError:
                messages.error(
                    request, 'You are already friends with this person')

    friends = Friend.objects.filter(user=request.user)
    print(friends)
    return render(request, "chatapp/add-friend.html",
                  {'form': f, 'friends': friends})


def home(request):
    return render(request, "chatapp/index.html", {})


def register(request):
    if request.method == 'POST':
        f = RegisterForm(request.POST)
        if f.is_valid():
            f.save()
            username = f.cleaned_data.get('username')
            password = f.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        f = RegisterForm()
    return render(request, 'chatapp/register.html', {'form': f})


@login_required
def userLogout(request):
    if request.method == 'POST':
        logout(request)
    return redirect('home')


def userLogin(request):
    if request.method == 'POST':
        f = LoginForm(request.POST)
        if f.is_valid():
            username = f.cleaned_data.get('username')
            password = f.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(
                    request, "There is no user with this user name and/or password")
    else:
        f = LoginForm()
    return render(request, 'chatapp/login.html', {'form': f})
