from django.shortcuts import render, redirect
from .models import Source, UserIncome
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
import datetime


def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText') 
        income = UserIncome.objects.filter(
            amount__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            pub_date__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            description__icontains=search_str, owner=request.user) | UserIncome.objects.filter(
            source__icontains=search_str, owner=request.user)
        
        data = income.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='/auth/login/')
def index(request):
    categories = Source.objects.all()
    income = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(income, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)       
    context = {
        'income': income,
        'page_obj': page_obj,        
    }
    return render(request, 'income/index.html', context)


@login_required(login_url='/auth/login/')
def add_income(request):
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST        
    }
    if request.method == 'GET':
        return render(request, 'income/add_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Сумма обязательна!')
            return render(request, 'income/add_income.html', context)

        description = request.POST['description']
        pub_date = request.POST['income_date']
        source = request.POST['source']

        if not description:
            messages.error(request, 'Описание обязательно!')
            return render(request, 'income/add_income.html', context)
        
        UserIncome.objects.create(owner=request.user, pub_date=pub_date, amount=amount,
                               source=source, description=description)       
        messages.success(request, 'Доход успешно сохранён!')
        return redirect('income')


@login_required(login_url='/auth/login/')
def income_edit(request, id):
    income = UserIncome.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        'income': income,
        'values': income,
        'sources': sources,
    }
    if request.method=='GET':        
        return render(request, 'income/edit_income.html', context)
    if request.method=='POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Сумма обязательна!')
            return render(request, 'income/edit_income.html', context)

        description = request.POST['description']
        pub_date = request.POST['income_date']
        source = request.POST['source']

        if not description:
            messages.error(request, 'Описание обязательно!')
            return render(request, 'income/edit_income.html', context)
        
        income.amount = amount
        income.pub_date = pub_date
        income.source = source
        income.description = description            
              
        income.save()      
        messages.success(request, 'Запись успешно обновлена!')

        return redirect('income')   


def delete_income(request, id):
    income = UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request, 'Запись удалёна!')

    return redirect('income') 
 

def income_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date - datetime.timedelta(days=30*6)
    expenses = UserIncome.objects.filter(owner=request.user,
                                      pub_date__gte=six_months_ago, pub_date__lte=todays_date)
    finalrep = {}

    def get_category(expense):
        return expense.source

    category_list = list(set(map(get_category, expenses)))
    
    def get_expense_category_amount(source):
        amount = 0
        filtered_by_category = expenses.filter(source=source)

        for item in filtered_by_category:
            amount += item.amount
        return amount

    for x in expenses:
        for y in category_list:
            finalrep[y] = get_expense_category_amount(y)
    return JsonResponse({'income_category_date': finalrep}, safe=False)


def stat_income_view(request):
    return render(request, 'income/stats_income.html')