from rest_framework.response import Response
from rest_framework.views import APIView
import yaml
import os



class OpenApiView(APIView):
    """
    Documentation.
    """
    def get(self, request):
        module_dir = os.path.dirname(__file__)  # get current directory
        file_path = os.path.join(module_dir, 'openapi-schema.yml')
        with open(file_path) as f:
            data1 = yaml.load(f)
        return Response(data1)
