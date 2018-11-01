from django.urls import path

from articles import views

app_name = 'articles'

urlpatterns = [
    path('read/<str:title>/', views.ArticleReadView.as_view()),
    path('add/', views.ArticleAddView.as_view()),
    path('edit/', views.ArticleEditView.as_view()),
    path('revisions/<str:title>/', views.RevisionsView.as_view()),
    path('all/', views.ArticlesListView.as_view()),

]


