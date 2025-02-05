from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.handlers.wsgi import WSGIRequest
from typing import Optional

from apps.auths.models import CustomUser

# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    fieldsets = (
        ('Information', {
            'fields': (
                'email',
                'password',
                'data_joined',
            )
        }),
        ('Permitions', {
            'fields': (
                'is_superuser',
                'is_staff',
                'is_active',
            ),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': (
                'wide',
            ),
            'fields': (
                'email',
                'password1',
                'password2',
                'is_active',
            ),
        }),
    )

    list_display = (
        'email',
        'data_joined',
        'is_staff',
        'is_active',
    )
    search_fields = (
        'email',
    )
    list_filter = (
        'email',
        'is_superuser',
        'is_staff',
    )
    ordering = (
        'email',
    )
    readonly_fields = (
        'data_joined',
        'is_superuser',
        'is_staff',
    )
    def get_readonly_fields(
        self, 
        request: WSGIRequest, 
        obj: Optional[CustomUser] = None
    ) -> tuple:
        if not obj:
            return self.readonly_fields
        
        return self.readonly_fields + (
            'email',
        )


admin.site.register(CustomUser, CustomUserAdmin)
