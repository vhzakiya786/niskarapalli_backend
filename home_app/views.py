from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.urls import reverse_lazy,reverse
from django.http import JsonResponse
from .models import Member, Donation, Subscription, Expense, ImamSalary
from .forms import MemberForm, DonationForm, SubscriptionForm, ExpenseForm, ImamSalaryForm
from django.db.models import Sum, Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from datetime import datetime, timedelta
import calendar

@method_decorator(login_required(login_url='login'), name='dispatch')
class DashboardView(ListView):
    model = Member
    template_name = 'dashboard.html'
    context_object_name = 'members'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(phone_number__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = int(self.request.GET.get('year', datetime.now().year))
        months = [(calendar.month_name[i], i) for i in range(1, 13)]
        members = self.get_queryset()
        subscription_data = []
        
        for member in members:
            subscriptions = Subscription.objects.filter(
                member=member,
                subscription_date__year=year
            ).values('subscription_date__month', 'amount')
            month_data = {m[1]: 'X' for m in months}
            for sub in subscriptions:
                month_data[sub['subscription_date__month']] = sub['amount']
            subscription_data.append({
                'member': member,
                'months': [(month_name, month_data[month_num]) for month_name, month_num in months]
            })
        context['subscription_data'] = subscription_data
        context['year'] = year
        context['years'] = range(2024, datetime.now().year + 1)
        context['member_form'] = MemberForm()
        context['search_query'] = self.request.GET.get('search', '')
        return context

    def post(self, request, *args, **kwargs):
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        return self.get(request, *args, **kwargs)

@method_decorator(login_required(login_url='login'), name='dispatch')
class ReportView(TemplateView):
    template_name = 'reports.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        period = self.request.GET.get('period', 'monthly')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        
        if period == 'custom' and start_date and end_date:
            try:
                start = datetime.strptime(start_date, '%Y-%m-%d')
                end = datetime.strptime(end_date, '%Y-%m-%d')
                if start > end:
                    raise ValueError("Start date must be before end date.")
                donations = Donation.objects.filter(donation_date__range=[start, end])
                subscriptions = Subscription.objects.filter(subscription_date__range=[start, end])
                expenses = Expense.objects.filter(expense_date__range=[start, end])
                salaries = ImamSalary.objects.filter(payment_date__range=[start, end])
            except (ValueError, TypeError) as e:
                context['error'] = str(e)
                donations = Donation.objects.none()
                subscriptions = Subscription.objects.none()
                expenses = Expense.objects.none()
                salaries = ImamSalary.objects.none()
        else:
            end = datetime.now()
            if period == 'monthly':
                start = end.replace(day=1)
            elif period == '6monthly':
                start = end - timedelta(days=180)
            else:  # yearly
                start = end.replace(month=1, day=1)
            donations = Donation.objects.filter(donation_date__range=[start, end])
            subscriptions = Subscription.objects.filter(subscription_date__range=[start, end])
            expenses = Expense.objects.filter(expense_date__range=[start, end])
            salaries = ImamSalary.objects.filter(payment_date__range=[start, end])
        
        total_donations = donations.aggregate(Sum('amount'))['amount__sum'] or 0
        total_subscriptions = subscriptions.aggregate(Sum('amount'))['amount__sum'] or 0
        total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        total_salaries = salaries.aggregate(Sum('amount'))['amount__sum'] or 0
        
        total_income = total_donations + total_subscriptions
        total_expenses_all = total_expenses + total_salaries
        net_balance = total_income - total_expenses_all
        
        context['total_donations'] = total_donations
        context['total_subscriptions'] = total_subscriptions
        context['total_income'] = total_income
        context['total_expenses'] = total_expenses
        context['total_salaries'] = total_salaries
        context['total_expenses_all'] = total_expenses_all
        context['net_balance'] = net_balance
        context['period'] = period
        return context

# ... (other imports and views remain unchanged)

@method_decorator(login_required(login_url='login'), name='dispatch')
class MemberView(View):
    template_name = 'members.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        query=request.GET.get('search','')
        if query:
            members = Member.objects.filter(
                Q(name__icontains=query) | Q(family_name__icontains=query) | Q(phone_number__icontains=query)
                ).order_by('name')
        else:
            members = Member.objects.all().order_by('name')

        page = request.GET.get('page', 1)
        from django.core.paginator import Paginator
        paginator = Paginator(members, self.paginate_by)
        members_page = paginator.get_page(page)

        member_id = request.GET.get('member_id')
        if member_id:
            member = Member.objects.filter(id=member_id).first()
            if member:
                form = MemberForm(instance=member, initial={
                    'name': member.name,
                    'phone_number': member.phone_number,
                    'email': member.email,
                    'family_name':member.family_name

                })
            else:
                form = MemberForm()
        else:
            member = Member.objects.none()
            form = MemberForm()

        context = {
            'members': members_page,
            'form': form,
            'selected_member_id': member_id,
            'selected_member_name': member.name if member else '',
            'selected_member_family_name': member.family_name if member else '',
            'selected_member_phone': member.phone_number if member else '',
            'selected_member_email': member.email if member else '',
            'current_page':page,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        member_id = request.POST.get('member_id')
        if member_id:
            member = Member.objects.filter(id=member_id).first()
            if not member:
                return redirect('members')
            form = MemberForm(request.POST, instance=member)
        else:
            form = MemberForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('members')
        
        members = Member.objects.all().order_by('name')
        page = request.GET.get('page', 1)
        from django.core.paginator import Paginator
        paginator = Paginator(members, self.paginate_by)
        members_page = paginator.get_page(page)

        context = {
            'members': members_page,
            'form': form,
            'selected_member_id': member_id,
            'selected_member_name': member.name if member else '',
            'selected_member_family_name': member.family_name if member else '',
            'selected_member_phone': member.phone_number if member else '',
            'selected_member_email': member.email if member else '',
            'current_page':page
        }
        return render(request, self.template_name, context)

def search_members(request):
    query = request.GET.get('q', '')
    members = Member.objects.filter(
        Q(name__icontains=query) | Q(family_name__icontains=query) | Q(phone_number__icontains=query)
    )[:10]
    results = [
        {
            'id': m.id,
            'name': m.name,
            'phone': m.phone_number,
            'email': m.email,
            'family_name':m.family_name
        } for m in members
    ]
    return JsonResponse({'results': results})

# ... (other views remain unchanged)
@method_decorator(login_required(login_url='login'), name='dispatch')
class DonationCreateView(CreateView):
    model = Donation
    form_class = DonationForm
    template_name = 'donations.html'
    success_url = reverse_lazy('donations')

    def post(self, request, *args, **kwargs):
        donation_id = request.GET.get('donation_id') or request.POST.get('donation_id')
        data=self.request.POST
        member=data.get('member')

        subscription=None

        if donation_id:
            subscription = Donation.objects.filter(id=donation_id).first()
            form = DonationForm(request.POST, instance=subscription)
        else:
            form = DonationForm(request.POST)

        if form.is_valid():
            form.save()
            url = reverse('donations') + f"?member={member}"

            return redirect(url)
        return redirect('donations')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member_id = self.request.GET.get("member")
        member=None
        donation_id = self.request.GET.get('donation_id')
        try:
            if member_id:
                member = Member.objects.get(id=member_id)
                if member:
                    values=Donation.objects.filter(member=member).values('id','member__name','amount','donation_date','purpose','payment_method','upi_id','transaction_id','is_anonymous')
                    payment_method='CASH'
                    if values.last():
                        payment_method=values.last().get("payment_method")
                    context['form'] = DonationForm(initial={'member': member,"payment_method":payment_method})
                else:
                    values=Donation.objects.values('id','member__name','amount','donation_date','purpose','payment_method','upi_id','transaction_id','is_anonymous')
            elif donation_id:
                instance=Donation.objects.get(id=donation_id)
                context['form'] = DonationForm(instance=instance)
                values=Donation.objects.filter(member=instance.member).values('id','member__name','amount','donation_date','purpose','payment_method','upi_id','transaction_id','is_anonymous')
            else:
                values=Donation.objects.values('id','member__name','amount','donation_date','purpose','payment_method','upi_id','transaction_id','is_anonymous')

            context['records'] = values
            context['total'] = values.aggregate(total=Sum('amount')).get('total')
        except Donation.DoesNotExist:
            pass
        return context 

@method_decorator(login_required(login_url='login'), name='dispatch')
class SubscriptionCreateView(CreateView):
    model = Subscription
    form_class = SubscriptionForm
    template_name = 'subscriptions.html'
    success_url = reverse_lazy('subscriptions')

    def post(self, request, *args, **kwargs):
        subscription_id = request.GET.get('subscription_id') or request.POST.get('subscription_id')
        data=self.request.POST
        member=data.get('member')
        subscription_date=data.get('subscription_date')
        duplicate=data.get('duplicate')
        subscription=None
        if member and subscription_date and not duplicate:
            year=subscription_date.split("-")[0]
            month=subscription_date.split("-")[1]
            subscription=Subscription.objects.filter(member=member,subscription_date__year=year,subscription_date__month=month).first()
        if subscription:
            form = SubscriptionForm(request.POST, instance=subscription)
        elif subscription_id:
            subscription = Subscription.objects.filter(id=subscription_id).first()
            form = SubscriptionForm(request.POST, instance=subscription)
        else:
            form = SubscriptionForm(request.POST)

        if form.is_valid():
            form.save()
            url = reverse('subscriptions') + f"?member={member}"

            return redirect(url)
        return redirect('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member_id = self.request.GET.get("member")
        subscription_id = self.request.GET.get("subscription_id")
        
        if member_id:
            try:
                member = Member.objects.get(id=member_id)
                values=Subscription.objects.filter(member=member).values('id','payment_method','upi_id','subscription_date','amount').order_by('subscription_date')
                payment_method='CASH'
                if values.last():
                    payment_method=values.last().get("payment_method")
                context['form'] = SubscriptionForm(initial={'member': member,"payment_method":payment_method})
                context['records'] = values
                context['total'] = values.aggregate(total=Sum('amount')).get('total')
            except Member.DoesNotExist:
                context['form'] = SubscriptionForm()
        elif subscription_id:
            instance=Subscription.objects.get(id=subscription_id)
            values=Subscription.objects.filter(member=instance.member).values('id','payment_method','upi_id','subscription_date','amount').order_by('subscription_date')
            context['form'] = SubscriptionForm(instance=instance)
            context['records'] = values
            context['total'] = values.aggregate(total=Sum('amount')).get('total')
        else:
            context['form'] = SubscriptionForm()

        return context                                                                                      

@method_decorator(login_required(login_url='login'), name='dispatch')
class ExpenseCreateView(CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expenses.html'
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            values=Expense.objects.values('amount','expense_date','purpose','payment_method','upi_id','transaction_id','notes')
            context['records'] = values
            context['total'] = values.aggregate(total=Sum('amount')).get('total')
        except Expense.DoesNotExist:
            pass
        return context  

@method_decorator(login_required(login_url='login'), name='dispatch')
class ImamSalaryCreateView(CreateView):
    model = ImamSalary
    form_class = ImamSalaryForm
    template_name = 'imam_salary.html'
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            values=ImamSalary.objects.values('amount','payment_date','payment_method','upi_id','transaction_id','notes')
            context['records'] = values
            context['total'] = values.aggregate(total=Sum('amount')).get('total')
        except ImamSalary.DoesNotExist:
            pass
 

        return context  

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages

def custom_login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard after login
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'admin_login.html')
def custom_logout(request):
    logout(request)
    return redirect('dashboard')

