
from rest_framework import routers

from home_app.views import TestViewset, UserViewset, user_create, user_edit, user_search
from django.urls import path
router=routers.SimpleRouter()



router.register(r'user',UserViewset,basename='user')
router.register(r'name',TestViewset,basename='test')
urlpatterns = [
    path('create/', user_create, name='user_create'),
    path('search/', user_search, name='user_search'),
    path('edit/<int:user_id>/', user_edit, name='user_edit'),
]
urlpatterns+=router.urls