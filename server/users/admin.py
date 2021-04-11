from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

@admin.register(get_user_model())
class CustomUserAdmin(UserAdmin):

    list_display = ('first_name', 'last_name', 'phone_number', 'type', 'is_active')
    list_filter = ('first_name', 'last_name', 'phone_number', 'type', 'is_active')
    fieldsets = (
        (None, {
            "fields": (
                'first_name', 'last_name', 'phone_number', 'type', 'password'
            ),
        }),
        ('Permissions', {'fields': ('is_staff', 'is_active')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            "fields": (
                'first_name', 'last_name', 'phone_number', 'type', 'password1', 'password2', 'is_active', 'is_staff'
            ),
        }),
    )

    search_fields = ('first_name', 'last_name', 'phone_number', 'type')
    ordering = ('type', )

# admin.site.register(get_user_model(), CustomUserAdmin)
    
