
from rest_framework import authentication,exceptions
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model

class CustomeJwtAuthentication(authentication.BaseAuthentication):

    authentication_header_prefix = 'Bearer'

    def authenticate(self, request):
        user=request.user
        auth_header=authentication.get_authorization_header(request).split()
        auth_header_prefix=self.authentication_header_prefix.lower()

        if not auth_header:
            return None
        
        if len(auth_header)==1:
            return None
        
        elif len(auth_header)>2:
            return None
        prefix=auth_header[0].decode('utf-8')
        token=auth_header[1].decode('utf-8')

        if prefix.lower() !=auth_header_prefix:
            return None
        
        return self._self_authenticate_credentials(request,token)
    
    def _self_authenticate_credentials(self,request,token):

        try:
            payload=jwt.decode(token,settings.SECRET_KEY,algorithms='HS256')
        except:
            msg = 'Invalid decoding token'
            raise exceptions.AuthenticationFailed(msg)
        User=get_user_model()
        try:
            if payload.get("user_id"):
                user=User.objects.filter(id=payload.get('user_id')).first()
                if not user:
                    return None
        except:
            return None
        if not user.is_active:
            return None
        return (user,None)

