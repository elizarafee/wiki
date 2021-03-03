from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("createentry", views.createEntry, name="createentry"),
    path("editentry/<str:title>", views.editEntry, name="editentry"),
    path("randomentry", views.randomEntry, name="randomentry"),
]
