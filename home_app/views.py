from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from home_app.models import UserModel
from home_app.serializers import UserSerializers
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication 

class UserViewset(viewsets.ModelViewSet):
    
    queryset=UserModel.objects.all()
    serializer_class=UserSerializers
    authentication_classes=[JWTAuthentication]

    def create(self, request, *args, **kwargs):
        data=request.data
        name=data.get("name")
        obj=UserModel.objects.filter(name=name).first()
        if obj:
            serializers=UserSerializers(obj,data=data, partial=True)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data)
        return super().create(request, *args, **kwargs)