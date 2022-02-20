from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView


class LogoutView(APIView):
    def get(self, request):
        request.user.auth_token.delete()

        return Response('Logged out!', status=status.HTTP_200_OK)

class TokenValidityView(APIView):
    def get(self, request):
        return Response('Valid token', status=status.HTTP_200_OK)