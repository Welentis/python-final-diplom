[Описание проекта](../README.md)

## Запуск проекта: 

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

## Запросы

1 **Регистрация**\
POST запрос
* url: http://127.0.0.1:8000/api/register
* Headers: -
* Body
  - username *
  - password *
  - email *
  - first_name 
  - last_name *
  - company
  - position
  - type (shop/buyer(по умолчанию)) *

ответ: статус код
на введенный email поступит сообщение с информацией о регистрации 

2 **Вход**\
POST запрос
* url: http://127.0.0.1:8000/api/login/
* Headers: -
* Body
  - username *
  - password *

ответ: статус код
  

3 **Выгрузка товаров**\
POST запрос
* url: http://127.0.0.1:8000/update/<file_name>
* Headers: {Authorization: <Token полученный на почту>}
* Body -

ответ: статус код
  

4 **Список товаров**\
Get запрос
* url: http://127.0.0.1:8000/api/products
* Headers: {Authorization: <Token полученный на почту>}
* Body -

ответ: json c товарами
  


5 **Карточка товара**\
Get запрос
* url: http://127.0.0.1:8000/api/products/<id>
* Headers: {Authorization: <Token полученный на почту>}
* Body -

ответ: json с информацией о товаре
  

6 **Корзина**\
Get запрос
* url: http://127.0.0.1:8000/api/order
* Headers: {Authorization: <Token полученный на почту>}
* Body -

ответ: json с товарами в карзине текущего юзера

POST запрос
* url: http://127.0.0.1:8000/api/order
* Headers: {Authorization: <Token полученный на почту>}
* Body 
  - product
  - shop
  - quantity

ответ: статус код


7 **Подтверждение заказа**\
POST запрос
* url: http://127.0.0.1:8000/api/orderConfirm
* Headers: {Authorization: Token myToken}
* Body 
  -  action (approve/disapprove)

ответ: статус код
