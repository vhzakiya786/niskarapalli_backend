
from rest_framework import routers

from home_app.views import TestViewset, UserViewset

router=routers.SimpleRouter()



router.register(r'user',UserViewset,basename='user')
router.register(r'test',TestViewset,basename='test')

urlpatterns=router.urls