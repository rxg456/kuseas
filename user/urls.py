from django.urls import path
from .views import menulist_view

urlpatterns = [
    path('menulist/', menulist_view)
]