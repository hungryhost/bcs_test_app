# Тестовое задание для BCSCHAIN
Развёрнуто на https://bcschain.yuryborodin.ru/

## Описание работы
На главной странице находится таблица с информацией о блоках блокчейна BCS Chain.

Доступен фильтр по дате. При этом, если на данную дату в БД не хранится инфомация,
то она подгружается из API.

При нажатии на height параметр в строке таблице можно перейти на страницу
более подробного описания блока, где находится ссылка на переход в админку, в которой можно редактировать
блок.

Помимо этого, каждую ночь в 00:30 включается автоматическая подгрузка данных на
предыдущий день с помощью Celery и Redis.

Для хранения данных используется PostgreSQL.

Для хранения static и медиа файлов используется Amazon S3.

## Развёртывание
Приложение развёрнуто на VPS с Ubuntu Server 18.04 LTS с помощью docker-compose.

Для воспроизведения результата необходимо следующее:
0) Сервер с установленными docker, docker-compose и nginx, с доменом с сертификатом 
1) Создать в папке bcproject файл .env следующего содержания
```
# base settings
DEBUG=off
ALLOWED_HOSTS=127.0.0.1,.localhost,<your_domain>
SECRET_KEY=<your key>
CORS_ORIGIN_ALLOW_ALL=False
CORS_ALLOWED_ORIGINS=<your_origins>
# log paths
LOG_ROOT=/bcsproject/logs
# database config
DB_NAME=<db_name>
# DB_HOST is the same as the one in docker-compose file
DB_HOST=db
DB_PORT=5432
DB_USER=<db_user>
DB_PASSWORD=<db_pass>

DJANGO_ADMIN_FNAME=<admin_user_first_name>
DJANGO_ADMIN_LNAME=<admin_user_last_name>
DJANGO_ADMIN_EMAIL=<admin_user_email>
DJANGO_ADMIN_PASSWORD=<admin_user_password>
# celery config in accordance with the docker-compose file
CELERY_BROKER_URL=redis://redis:6379
CELERY_RESULT_BACKEND=redis://redis:6379
# storage settings
# whether to use postgres or sqlite3
USE_POSTGRES=True
# whether to host static and media files on S3
USE_S3=True
AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>
AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>
AWS_STORAGE_BUCKET_NAME=<AWS_BUCKET_NAME>
AWS_S3_ENDPOINT_URL=<AWS_ENDPOINT>
```

2) Заполнить .env файл в папке postgres:
```
POSTGRES_USER=<db_user>
POSTGRES_PASSWORD=<db_pass>
POSTGRES_DB=<db_name>
```
3) Запустить команду ``` docker-compose up -d ```