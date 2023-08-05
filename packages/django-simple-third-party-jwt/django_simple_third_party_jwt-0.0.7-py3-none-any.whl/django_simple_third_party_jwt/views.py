from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.views import TokenObtainPairView

from django_simple_third_party_jwt.serializers import SocialLoginSerializer

from django_simple_third_party_jwt.exception import InvalidEmailError

import logging

logger = logging.getLogger(__name__)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh_token": str(refresh),
        "access_token": str(refresh.access_token),
        # compatibility with official Simple JWT
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class GoogleLogin(TokenObtainPairView):
    permission_classes = (AllowAny,)  # AllowAny for login
    serializer_class = SocialLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                user = serializer.save()
                return Response(get_tokens_for_user(user))
            except InvalidEmailError:
                return Response(
                    {"status": "error", "detail": "This email is invaild."}, status=401
                )
            except ValueError as e:
                logger.error(e)
                return Response(
                    {"status": "error", "detail": "Something wnet wrong :("}, status=500
                )
        else:
            return Response(
                {"status": "error", "detail": "Data is not serializable"}, status=401
            )
