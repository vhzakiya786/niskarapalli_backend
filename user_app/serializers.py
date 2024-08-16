
from typing import Any, Dict
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class LoginSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls,user):
        token=super().get_token(user)

        return token
    
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)

        return data