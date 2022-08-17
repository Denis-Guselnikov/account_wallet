# "Кошелёк расходов и доходов"

## Wallet.
- "Wallet" позволяет создавать, редактировать и удалять записи.
- Благодаря Графам можно наглядно получить информацию введёнными вами данными.

## В проекте используется:
- Django 3
- Bootstrap 5
- Chart.js
- Python 3.7.9
- HTML 5
- CSS
- JavaScript 

# Установка проекта:
## Клонировать репозиторий и перейти в него в командной строке:
- git clone https://github.com/Denis-Guselnikov/account_wallet
- cd account wallet/
## Cоздание виртуального окружения и его активация:
- python -m venv venv
- source venv/Scripts/activate
## Установка зависимостей из requirements.txt:
- pip install -r requirements.txt
## Выполнение миграций:
- python manage.py migrate
## Запуск проекта:
- cd wallet/
- python3 manage.py runserver
