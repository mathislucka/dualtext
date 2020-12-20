from rest_framework.views import APIView
from rest_framework.response import Response
from dualtext_api.serializers import UserSerializer
from dualtext_api.services import UserService

class CurrentUserView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class CurrentUserStatisticsView(APIView):
    def get(self, request):
        us = UserService(self.request.user.id)
        stats = us.get_user_statistics()
        return Response(stats)
