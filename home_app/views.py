from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from home_app.models import UserModel
from home_app.serializers import UserSerializers
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication 
from django.shortcuts import render, get_object_or_404, redirect
from .models import UserModel
from .forms import UserModelForm
from django.db.models import Q
from rest_framework.decorators import action
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

class TestViewset(viewsets.ModelViewSet):
    
    queryset=UserModel.objects.all()
    serializer_class=UserSerializers
    authentication_classes=[]
    permission_classes = []

    http_method_names = ['get',]

    def list(self, request, *args, **kwargs):
        search=request.GET.get("search")

        if search:
            self.queryset=self.queryset.filter(name__icontains=search)
        return super().list(request, *args, **kwargs)

    @action(methods=['post','get'],detail=False)
    def user_search(self,request,**kwargs):
        query = request.GET.get('q', '')
        if query:
            users = UserModel.objects.filter(
                Q(name__icontains=query) | Q(mobile__icontains=query)
            )
        else:
            users = UserModel.objects.all()

        context = {
            'users': users,
            'query': query,
        }
        return render(request, 'user_search.html', context)

    @action(methods=['post','get'],detail=True)
    def user_edit(self,request, user_id):
        user = get_object_or_404(UserModel, id=user_id)
        if request.method == 'POST':
            form = UserModelForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect('user_search')
        else:
            form = UserModelForm(instance=user)

        context = {
            'form': form,
            'user': user,
        }
        return render(request, 'user_edit.html', context)

def user_search(request):
    query = request.GET.get('q', '')
    if query:
        users = UserModel.objects.filter(
            Q(name__icontains=query) | Q(mobile__icontains=query)
        )
    else:
        users = UserModel.objects.all()

    context = {
        'users': users,
        'query': query,
    }
    return render(request, 'user_search.html', context)

from django.core.exceptions import ValidationError
from .models import UserModel

def user_edit(request, user_id):
    user = get_object_or_404(UserModel, id=user_id)
    
    if request.method == 'POST':
        selected_month = request.POST.get('month')
        amount = request.POST.get('amount')
        
        if selected_month and amount:
            try:
                # Convert amount to a Decimal, ensuring it's valid
                from decimal import Decimal
                decimal_amount = Decimal(amount)
                
                # Set the value for the selected month
                setattr(user, selected_month, decimal_amount)
                user.save()
                
                return redirect('user_search')
            except (ValueError, ValidationError, ArithmeticError) as e:
                # Handle conversion errors
                return render(request, 'user_edit.html', {
                    'user': user,
                    'selected_month': selected_month,
                    'error_message': str(e),
                    'months': ['jan', 'feb', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'],
                })
        else:
            return render(request, 'user_edit.html', {
                'user': user,
                'selected_month': selected_month,
                'error_message': 'Amount cannot be empty.',
                'months': ['jan', 'feb', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'],
            })
    else:
        selected_month = request.GET.get('month', 'jan')

    context = {
        'user': user,
        'selected_month': selected_month,
        'months': ['jan', 'feb', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'],
    }
    return render(request, 'user_edit.html', context)


def user_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        
        # Optionally, set default values for monthly fields if needed
        UserModel.objects.create(
            name=name,
            mobile=mobile,
            jan=None,
            feb=None,
            march=None,
            april=None,
            may=None,
            june=None,
            july=None,
            august=None,
            september=None,
            october=None,
            november=None,
            december=None
        )
        return redirect('user_search')
    
    return redirect('user_search')    