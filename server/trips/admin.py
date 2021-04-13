from django.contrib import admin
# from django.contrib.auth import get_user_model
# from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import Trip

# @admin.register(get_user_model())
# class UserAdmin(DefaultUserAdmin):
#     pass

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    fields = ('id', 'pickup', 'dropoff', 'status', 'rider', 'driver', 'created', 'updated',)
    list_display = ('id', 'pickup', 'dropoff', 'status', 'rider', 'driver', 'created', 'updated',)
    list_filter = ('status', )
    readonly_fields = ('id', 'created', 'updated')

