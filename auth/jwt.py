import jwt
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.encoding import smart_text

User = get_user_model()


class JWTAuthentication(object):
    def get_jwt_value(self, request):
        auth = request.META["HTTP_AUTHORIZATION"].split()
        auth_header_prefix = settings.JWT_AUTH_HEADER_PREFIX.lower()

        if len(auth) != 2:
            return

        if smart_text(auth[0].lower()) != auth_header_prefix:
            return None

        return auth[1]

    def authenticate(self, request):
        print('JWT AUTH::')
        jwt_value = self.get_jwt_value(request)
        if jwt_value is None:
            return None

        payload = jwt.decode(jwt_value, key=settings.JWT_SECRET)
        user_id = payload['user_id']
        username = payload['username']

        try:
            request.user = User.objects.get(id=user_id, username=username)
        except User.DoesNotExist:
            return None
        print('user:::', request.user)
        return request.user
