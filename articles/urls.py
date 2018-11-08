from django.urls import path

from articles import views

app_name = 'articles'


urlpatterns = [
    path('', views.ArticlesListView.as_view()),
    path('read/<int:pk>/', views.ArticleReadView.as_view()),
    path('add/', views.ArticleAddView.as_view()),
    path('edit/', views.ArticleEditView.as_view()),
    path('revisions/<int:article_id>/', views.RevisionsView.as_view()),

]

