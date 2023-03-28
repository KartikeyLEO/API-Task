from django.contrib import admin
from .models import Employees, CustomToken


@admin.register(Employees)
class EmpAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'city', 'contact']


@admin.register(CustomToken)
class CustomTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'token_key', 'created_at', 'expires_at']
