
from rest_framework import routers

from django.urls import path
from .views import (
    DashboardView, MemberView, ReportView, DonationCreateView,
    SubscriptionCreateView, ExpenseCreateView, ImamSalaryCreateView, search_members,custom_login_view,custom_logout
)

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('login/', custom_login_view, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('reports/', ReportView.as_view(), name='reports'),
    path('members/', MemberView.as_view(), name='members'),
    # path('members/', MemberCreateView.as_view(), name='members'),
    path('offers/', DonationCreateView.as_view(), name='offers'),
    path('subscriptions/', SubscriptionCreateView.as_view(), name='subscriptions'),
    path('expenses/', ExpenseCreateView.as_view(), name='expenses'),
    path('imam-salary/', ImamSalaryCreateView.as_view(), name='imam_salary'),
    path('search-members/', search_members, name='search_members'),
]
# urlpatterns=urlpatterns+router.urls