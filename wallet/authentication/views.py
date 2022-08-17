from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
import json
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.urls import reverse
from .utils import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import auth



class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email недействителен!'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Email уже используется, выбери другой!'}, status=409)
        return JsonResponse({'email_valid': True})


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Имя пользователя должно содержать только буквенно-цифровые символы!'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Имя уже используется, выбери другое!'}, status=409)
        return JsonResponse({'username_valid': True})


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):        

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST,
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, "Слишком короткий пароль!")
                    return render(request, 'authentication/register.html', context)
                
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False                
                user.save()
                current_site = get_current_site(request)
                email_body = {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                }

                link = reverse('activate', kwargs={
                               'uidb64': email_body['uid'], 'token': email_body['token']})

                email_subject = 'Activate your account'

                activate_url = 'http://'+current_site.domain+link

                email = EmailMessage(
                    email_subject,
                    'Hi '+user.username + ', Please the link below to activate your account \n'+activate_url,
                    'testsend152@gmail.com',
                    [email],
                )
                email.send(fail_silently=True)
                messages.success(request, "Аккаунт успешно создан!")
                return render(request, 'authentication/register.html')


        return render(request, 'authentication/register.html')               

class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except Exception as ex:
            pass

        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Добро пожаловать '+user.username+ ' ,вы вошли в систему!')
                    return redirect('expenses')
                messages.error(request, 'Аккаунт не активен, проверь почту!')
                return render(request, 'authentication/login.html')
            messages.error(request, 'Попробуй ещё!')
            return render(request, 'authentication/login.html')
        messages.error(request, 'Заполните все поля!')
        return render(request, 'authentication/login.html')


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'Ты вышел из системы')
        return redirect('login')


class RequestPasswordResetEmail(View):
    def get(self, request):        
        return render(request, 'authentication/reset-password.html')

    def post(self, request):
        email = request.POST['email'] 

        context = {
            'values': request.POST
        } 

        if not validate_email(email):
            messages.error(request, 'Пожалуйста, укажите действительный адрес электронной почты')
            return render(request, 'authentication/reset-password.html', context) 

        current_site = get_current_site(request)

        user = request.objects.filter
        email_body = {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        }

        link = reverse('activate', kwargs={
                       'uidb64': email_body['uid'], 'token': email_body['token']})

        email_subject = 'Activate your account'

        activate_url = 'http://'+current_site.domain+link

        email = EmailMessage(
            email_subject,
            'Hi '+user.username + ', Please the link below to activate your account \n'+activate_url,
            'testsend152@gmail.com',
            [email],
        )
        email.send(fail_silently=False)
