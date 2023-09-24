FROM alpine:latest

ENV DEBUG 1
ENV SECRET_KEY django-insecure-933a@6e9c5rfsyh2vthl8e4b*5m$x@6khd&_-ariip*tyk(g&n

ENV SQL_ENGINE django.db.backends.postgresql
ENV SQL_DATABASE diplom_db
ENV SQL_USER postgres
ENV SQL_PASSWORD postgres
ENV SQL_HOST localhost
ENV SQL_PORT 5432

ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD postgres
ENV POSTGRES_DB diplom_db

ENV EMAIL_HOST smtp.mail.ru
ENV EMAIL_HOST_USER test_dip_nt@example.com
ENV EMAIL_HOST_PASSWORD mXqbzXs4cfZSnFtx3gtC
ENV EMAIL_PORT 465
ENV EMAIL_USE_SSL True

ENV DJANGO_SUPERUSER_USERNAME admin
ENV DJANGO_SUPERUSER_PASSWORD admin
ENV DJANGO_SUPERUSER_EMAIL admin@example.com

RUN apk update
RUN apk add postgresql openrc python3 nginx curl
RUN python3 -m ensurepip
RUN mkdir /run/postgresql
RUN chown postgres:postgres /run/postgresql
RUN su - postgres -c "mkdir /var/lib/postgresql/data"
RUN su - postgres -c "chmod 0700 /var/lib/postgresql/data"
RUN su - postgres -c "initdb -D /var/lib/postgresql/data"

COPY /custom.start /etc/local.d/custom.start
RUN chmod +x /etc/local.d/custom.start

RUN rm /etc/nginx/http.d/default.conf
COPY nginx.conf /etc/nginx/http.d/

EXPOSE 80

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV HOME=/app
ENV APP_HOME=/app/web
RUN mkdir $HOME
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
WORKDIR $APP_HOME
RUN pip3 install --upgrade pip
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt
COPY ./orders .

ENTRYPOINT /etc/local.d/custom.start

VOLUME /var/lib/postgresql/data/
