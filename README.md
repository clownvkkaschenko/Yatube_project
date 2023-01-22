<div id="header" align="center">
  <h1>Проект YaTube</h1>
  <img src="https://img.shields.io/badge/Python-3.7.9-brightgreen"/>
  <img src="https://img.shields.io/badge/Django-2.2.19-blueviolet"/>
</div>

Cоциальная сеть YaTubeProject позволяет пользователям создавать учетную запись, публиковать посты и подписываться на любимых авторов.

### Запуск проекта:
- Клонируйте репозиторий и перейдите в него
    ```
    git clone git@github.com:clownvkkaschenko/Yatube_project.git
    ```
- Установите и активируйте виртуальное окружение
    ```
    python -m venv venv
    source venv/Scripts/activate
    ```
- Установите зависимости из файла requirements.txt
    ```
    pip install -r requirements.txt
    ``` 
- Перейдите в папку **yatube** с файлом manage.py, выполните миграции, и запустите сервер:
    ```
    python manage.py makemigrations
    python manage.py migrate

    python manage.py runserver
    ```

После этого проект будет доступен по url-адресу 127.0.0.1:8000
