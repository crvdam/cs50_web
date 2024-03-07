from django.urls import path

from . import views


app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:entry>/", views.entry, name="entry"),
    path("create", views.create, name='create'),
    path("randomentry", views.randomentry, name="randomentry"),
    path("search", views.search, name="search"),
    path("edit/<str:entry>", views.edit, name="edit"),
    
    
]
