# Generated by Django 3.1.2 on 2021-04-22 18:40

from django.db import migrations
import hashid_field.field


class Migration(migrations.Migration):

    dependencies = [
        ('userAccount', '0004_auto_20210422_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internaluser',
            name='unique_user_token',
            field=hashid_field.field.HashidField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=50, null=True, prefix=''),
        ),
    ]
