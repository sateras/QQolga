from django.contrib import admin
from apps.core.models import Card, Transactions, CustomUser, Post

# Register your models here.


class BankAccountAdmin(admin.ModelAdmin):
    pass

class CardAdmin(admin.ModelAdmin):
    list_display = (
        'account',
        'number'
    )
    list_filter = (
        'account',
        'number',
        'expiration_date',
    )


class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'sender',
        'receiver',
        'date',
    )
    list_filter = (
        'sender',
        'receiver',
        'status',
    )


admin.site.register(Card, CardAdmin)
admin.site.register(Transactions, TransactionAdmin)
admin.site.register(Post, BankAccountAdmin)