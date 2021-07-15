#!/bin/sh
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

echo "from django.contrib.auth import get_user_model;
User = get_user_model()
User.objects.filter(email='$DJANGO_ADMIN_EMAIL').delete();
User.objects.create_superuser(first_name='$DJANGO_ADMIN_FNAME', last_name='$DJANGO_ADMIN_LNAME', email='$DJANGO_ADMIN_EMAIL', password='$DJANGO_ADMIN_PASSWORD')" | python manage.py shell

exec "$@"