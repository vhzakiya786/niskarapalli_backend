
from rest_framework import routers

from home_app.views import UserViewset

router=routers.SimpleRouter()



router.register('user',UserViewset,basename='user')

urlpatterns=router.urls