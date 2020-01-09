from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from model import oss
from serializers import Serializer


# 使用APIView
class OssView(APIView):
    def get(self, request, format=None):
        product = oss.MOOSEMeta.objects.all()
        serializer = Serializer(product, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
