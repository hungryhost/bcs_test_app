from django.contrib import admin
from .models import Block
# Register your models here.


@admin.register(Block)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("hash", "height", "iso_timestamp")
    list_filter = ("iso_timestamp",)