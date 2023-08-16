from django.contrib import admin
from .models import Client, Event, Catalog, Consultation, Order

# Register your models here.

admin.site.register(Client)
admin.site.register(Event)
admin.site.register(Catalog)
admin.site.register(Consultation)
admin.site.register(Order)
