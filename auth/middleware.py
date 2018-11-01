import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin
from django.utils.encoding import smart_text
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.middleware import get_user
from django.contrib import auth

User = get_user_model()


class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.user = SimpleLazyObject(lambda: self.__class__.get_jwt_user(request))

    @staticmethod
    def get_jwt_token(request):
        auth = request.META["HTTP_AUTHORIZATION"].split()
        auth_header_prefix = settings.JWT_AUTH_HEADER_PREFIX.lower()

        if len(auth) != 2:
            return

        if smart_text(auth[0].lower()) != auth_header_prefix:
            return None

        return auth[1]

    @staticmethod
    def get_jwt_user(request):
        print('get jwt user')
        user_jwt = get_user(request)
        print('user_jwt', [user_jwt], user_jwt.is_authenticated)
        if user_jwt.is_authenticated:
            return user_jwt

        jwt_value = JWTAuthenticationMiddleware.get_jwt_token(request)
        print('token', [jwt_value])

        payload = jwt.decode(jwt_value, key=settings.JWT_SECRET)
        user_id = payload['user_id']
        username = payload['username']

        user_jwt = User.objects.get(id=user_id, username=username)

        return user_jwt
