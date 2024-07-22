from django.urls import path

from .views import new_day


urlpatterns = [
    path("new-day", new_day, name="new_day"),
]
