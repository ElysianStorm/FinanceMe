from django.contrib import admin
from .models import CustomUser, Category, CategoryReference, UserCategories, Transaction, TrackIncomeExpense, BudgetPlan

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(CategoryReference)
admin.site.register(UserCategories)
admin.site.register(Transaction)
admin.site.register(TrackIncomeExpense)
admin.site.register(BudgetPlan)