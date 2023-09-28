[Описание проекта](../README.md)

# Добавлен docker-compose
### Запуск проекта через докер:
1. Склонировать репозиторий
```bash
git clone https://github.com/Welentis/python-final-diplom.git
```
2. Запустить сборку контейнера
```bash
docker-compose up -d --build
```
3. Провести миграции моделей
```bash
docker-compose exec web python manage.py migrate --noinput
```
4. Сложить статические файлы в каталог, для корректного отображения страниц
```bash
docker-compose exec web python manage.py collectstatic --no-input --clear
```
5. В дальнейшем, для проверки, использовать ссылку:
```bash
http://127.0.0.1:8080
```




### Запросы

1 **Регистрация**\
POST запрос
* url: http://127.0.0.1:8080/api/register
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
* url: http://127.0.0.1:8080/api/login/
* Headers: -
* Body
  - username *
  - password *

ответ: статус код
  

3 **Выгрузка товаров**\
POST запрос
* url: http://127.0.0.1:8080/update/<file_name>
* Headers: {Authorization: <Token полученный на почту>}
* Body -

ответ: статус код
  

4 **Список товаров**\
Get запрос
* url: http://127.0.0.1:8080/api/products
* Headers: {Authorization: <Token полученный на почту>}
* Body -

ответ: json c товарами
  


5 **Карточка товара**\
Get запрос
* url: http://127.0.0.1:8080/api/products/<id>
* Headers: {Authorization: <Token полученный на почту>}
* Body -

ответ: json с информацией о товаре
  

6 **Корзина**\
Get запрос
* url: http://127.0.0.1:8080/api/order
* Headers: {Authorization: <Token полученный на почту>}
* Body -

ответ: json с товарами в карзине текущего юзера

POST запрос
* url: http://127.0.0.1:8080/api/order
* Headers: {Authorization: <Token полученный на почту>}
* Body 
  - product
  - shop
  - quantity

ответ: статус код


7 **Подтверждение заказа**\
POST запрос
* url: http://127.0.0.1:8080/api/orderConfirm
* Headers: {Authorization: Token myToken}
* Body 
  -  action (approve/disapprove)

ответ: статус код
