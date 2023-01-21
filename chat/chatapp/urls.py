from django.urls import path
from . import views
# fmt: off
urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register, name='register'),
    path('logout/', views.userLogout, name='logout'),
    path('login/', views.userLogin, name='login'),
    path('add-friend/', views.addFriend, name='add-friend'),
    path('chat/unexpected-disconnect', views.unexpectedDisconnect, name="unexpected-disconnect",),
    path('chat/<int:id>', views.chat, name='chat'),
    path('chat/', views.chat, name='chat'),
    path('old-messages/<str:roomName>/<int:page>', views.oldMessages, name='old-messages'),
    path('unfriend/', views.unfriend, name='unfriend')
]
# fmt: on
