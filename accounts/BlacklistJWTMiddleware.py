from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import BlacklistedToken
from rest_framework.exceptions import AuthenticationFailed


class BlacklistJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Call the base class to perform the usual authentication process
        user_auth_tuple = super().authenticate(request)

        if user_auth_tuple is not None:
            user, auth_token = user_auth_tuple

            # Check if the token is blacklisted
            if BlacklistedToken.objects.filter(token=auth_token).exists():
                raise AuthenticationFailed('Token is blacklisted. Please log in again.')

        return user_auth_tuple
