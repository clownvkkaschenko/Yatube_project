# Проект YaTube
### Описание
- Социальная сеть даст пользователям возможность создавать учетную запись, публиковать посты и подписываться на любимых авторов.
### Запуск проекта в dev-режиме:
- Клонируйте репозиторий и перейдите в него
- Установите и активируйте виртуальное окружение
- Установите зависимости из файла requirements.txt
    ```
    $ pip install -r requirements.txt
    ``` 
- В папке с файлом manage.py выполните миграции, и запустите сервер:
    ```
    $ python manage.py migrate
    ``` 
    ```
    $ python manage.py runserver
    ```
### Используемые технологии:
- [Python 3.7.9](https://www.python.org/)
- [Django 2.2.19](https://www.djangoproject.com/)
- [Social auth app django 5.0.0](https://python-social-auth.readthedocs.io/en/latest/configuration/django.html)
### Автор
Иван Конышкин
