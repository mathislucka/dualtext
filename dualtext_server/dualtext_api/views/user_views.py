from rest_framework.views import APIView
from rest_framework.response import Response
from dualtext_api.serializers import UserSerializer

class CurrentUserView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
