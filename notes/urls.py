from django.urls import path

from . import views

app_name = 'notes'

urlpatterns = [
    path('', views.NotesListView.as_view()),
    path('new/', views.NoteAddView.as_view()),
    path('<int:pk>/', views.NoteFetchView.as_view()),
    path('edit/<int:pk>/', views.NoteEditView.as_view()),
    path('delete/<int:pk>/', views.NoteDeleteView.as_view()),
]
