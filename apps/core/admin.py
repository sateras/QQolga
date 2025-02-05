from django.contrib import admin
from apps.core.models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'owner',
        'category',
        'price',
        'date_created'
    )
    list_filter = (
        'category',
        'date_created'
    )
    search_fields = (
        'title',
        'text',
        'phone'
    )
    ordering = (
        '-date_created',
    )
    readonly_fields = (
        'date_created',
    )


admin.site.register(Post, PostAdmin)
