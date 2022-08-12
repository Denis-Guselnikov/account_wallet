from django.shortcuts import render
import os
import json
from django.conf import settings
# from .models import UserePreferences
from userpreferences.models import UserePreferences
from django.contrib import messages



def index(request):

    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')

    
    with open(file_path, 'r') as json_file:                                         # r - read
        data = json.load(json_file)
        for k,v in data.items():
            currency_data.append({'name': k, 'value': v})

    exists = UserePreferences.objects.filter(user=request.user).exists()
    user_preferences = None

    if exists:
        user_preferences = UserePreferences.objects.get(user=request.user)

    if request.method=='GET':         
        return render(request, 'preferences/index.html', {'currencies': currency_data, 'user_preferences': user_preferences})

    else:
        currency = request.POST['currency']

        if exists:                       
            user_preferences.currency = currency 
            user_preferences.save()        
        else:
            UserePreferences.objects.create(user=request.user, currency=currency)
        messages.success(request, 'Изменения сохранены')        
        return render(request, 'preferences/index.html', {'currencies': currency_data, 'user_preferences': user_preferences})

    

    

    