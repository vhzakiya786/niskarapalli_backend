from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import Member, Donation, Subscription, Expense, ImamSalary
from .forms import MemberForm, DonationForm, SubscriptionForm, ExpenseForm, ImamSalaryForm
from django.db.models import Sum, Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from datetime import datetime, timedelta
import calendar

@method_decorator(login_required, name='dispatch')
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
        context['years'] = range(2020, datetime.now().year + 1)
        context['member_form'] = MemberForm()
        context['search_query'] = self.request.GET.get('search', '')
        return context

    def post(self, request, *args, **kwargs):
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        return self.get(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class ReportView(TemplateView):
    template_name = 'reports.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        period = self.request.GET.get('period', 'monthly')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        
        if period == 'custom' and start_date and end_date:
            donations = Donation.objects.filter(donation_date__range=[start_date, end_date])
            expenses = Expense.objects.filter(expense_date__range=[start_date, end_date])
            salaries = ImamSalary.objects.filter(payment_date__range=[start_date, end_date])
        else:
            end = datetime.now()
            if period == 'monthly':
                start = end.replace(day=1)
            elif period == '6monthly':
                start = end - timedelta(days=180)
            else:  # yearly
                start = end.replace(month=1, day=1)
            donations = Donation.objects.filter(donation_date__range=[start, end])
            expenses = Expense.objects.filter(expense_date__range=[start, end])
            salaries = ImamSalary.objects.filter(payment_date__range=[start, end])
        
        total_donations = donations.aggregate(Sum('amount'))['amount__sum'] or 0
        total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        total_salaries = salaries.aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Calculate net balance: Donations (incoming) - Expenses (outgoing) - Salaries (outgoing)
        net_balance = total_donations - total_expenses - total_salaries
        
        context['total_donations'] = total_donations
        context['total_expenses'] = total_expenses
        context['total_salaries'] = total_salaries
        context['net_balance'] = net_balance
        context['period'] = period
        return context

def search_members(request):
    query = request.GET.get('q', '')
    members = Member.objects.filter(name__icontains=query)[:10]
    results = [{'id': m.id, 'name': m.name, 'phone': m.phone_number} for m in members]
    return JsonResponse({'results': results})

class MemberCreateView(CreateView):
    model = Member
    form_class = MemberForm
    template_name = 'members.html'
    success_url = reverse_lazy('dashboard')

class DonationCreateView(CreateView):
    model = Donation
    form_class = DonationForm
    template_name = 'donations.html'
    success_url = reverse_lazy('dashboard')

class SubscriptionCreateView(CreateView):
    model = Subscription
    form_class = SubscriptionForm
    template_name = 'subscriptions.html'
    success_url = reverse_lazy('dashboard')

class ExpenseCreateView(CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expenses.html'
    success_url = reverse_lazy('dashboard')

class ImamSalaryCreateView(CreateView):
    model = ImamSalary
    form_class = ImamSalaryForm
    template_name = 'imam_salary.html'
    success_url = reverse_lazy('dashboard')