from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from auth import views

urlpatterns = [
    path('registration/', views.RegistrationView.as_view()),
    path('gettoken/', obtain_jwt_token),

]