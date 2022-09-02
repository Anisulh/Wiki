from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry_page, name= "entry_page"),
    path("create_page/", views.create_page, name= "create_page"),
    path("search/", views.search, name="search"),
    path("random/", views.random, name="random"),
    path("editpage/<str:title>", views.edit_page, name="edit_page"),
    path("login/", views.login, name = "login"),
    path("register/", views.register, name = "register"),
    path("logout/", views.logout, name = "logout")
]
