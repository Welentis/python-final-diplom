[Описание проекта](../README.md)

Запуск проекта: 

1. Создать виртуальное окружение, установить зависимости, при необходимости поменять значения в `orders/.env`
2. Создать базу данных 
```bash
createdb -U postgres diplom_db
```
3. Провести миграции 
```bash
python orders/manage.py makemigrations
python orders/manage.py migrate
```
4. Запустить приложение 
```bash 
python orders/manage.py runserver
```
