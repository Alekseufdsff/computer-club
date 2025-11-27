from django.contrib import admin
from .models import *

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'phone']

@admin.register(Computer)
class ComputerAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'status', 'is_public']

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at']

@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_active']

@admin.register(InternTask)
class InternTaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'assigned_to', 'is_completed']

@admin.register(ComputerRequest)
class ComputerRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'computer', 'is_processed']