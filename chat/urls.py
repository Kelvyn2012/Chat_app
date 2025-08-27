from django.urls import path
from .views import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("room/<slug:room_name>/", views.room, name="room"),
]
