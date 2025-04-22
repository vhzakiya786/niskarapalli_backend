
from rest_framework import routers

from home_app.views import TestViewset, UserViewset, user_create, user_edit, user_search
from . import views

from . import views
from home_app.views import TestViewset, UserViewset
from django.urls import path
router=routers.SimpleRouter()



router.register(r'user',UserViewset,basename='user')
router.register(r'name',TestViewset,basename='test')
urlpatterns = [
    path('create/', user_create, name='user_create'),
    path('search/', user_search, name='user_search'),
    path('edit/<int:user_id>/', user_edit, name='user_edit'),
    path('', views.user_create_update, name='user_create_update'),
    path('get_users/', views.get_users, name='get_users'),
    path('get_upi_ids/', views.get_upi_ids, name='get_upi_ids'),
    path('check_user_by_upi/', views.check_user_by_upi, name='check_user_by_upi'),
]

urlpatterns=urlpatterns+router.urls