from rest_framework import serializers

from home_app.models import UserModel


class UserSerializers(serializers.ModelSerializer):
    
    class Meta:
        model =UserModel
        exclude = ('created_at','updated_at')