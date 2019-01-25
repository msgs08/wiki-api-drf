import time

from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token

from . import views

#
# def obtain_jwt_token_wrapper(*args, **kwargs):
#     time.sleep(6)
#     print('wrpper')
#
#     return obtain_jwt_token(*args, **kwargs)

urlpatterns = [
    path('registration/', views.RegistrationView.as_view()),
    path('api-token-auth/', obtain_jwt_token),
    path('api-token-verify/', verify_jwt_token),
]
