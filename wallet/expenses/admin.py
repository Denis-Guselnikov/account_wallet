from django.contrib import admin
from .models import Expense, Category


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('owner', 'amount', 'description', 'category', 'pub_date')
    search_fields = ('category',)    
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'

admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Category)
