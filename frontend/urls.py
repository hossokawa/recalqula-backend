from django.urls import path
from . import views

urlpatterns = [
    # This path will catch all requests that haven't been matched by other Django URLs
    # and direct them to the React app's index.html.
    # This is crucial for client-side routing within your React app.
    path("", views.index, name="index"),
]
