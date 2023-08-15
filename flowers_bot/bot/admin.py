from django.contrib import admin
from .models import Client

# Register your models here.

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    search_fields = ['first_name','last_name','phone','address']
    list_filter = ['is_florist','is_courier']
    list_display = ['first_name','last_name','phone']