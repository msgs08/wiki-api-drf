from django.urls import path

from posts.views import PostAddView

app_name = 'posts'

urlpatterns = [
    path('new', PostAddView.as_view())
]
