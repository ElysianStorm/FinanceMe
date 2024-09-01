from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

def user_dir(instance, filename):
    return "usr_{0}/p_img".format(instance.username, filename)

class CustomUser(AbstractUser):
    PROFESSION = (
        ('service', 'Service'),
        ('business', 'Business'),
        ('freelance', 'Freelance'),
        ('others', 'Others')
    )

    username = models.CharField(unique=True, max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    profession = models.CharField(max_length=20, choices=PROFESSION)
    p_image = models.FileField(upload_to=user_dir)

    def __str__(self) -> str:
        return super().__str__()

class Category(models.Model):
    cat_name = models.CharField(unique=True, max_length=500)
    cat_desc = models.TextField(max_length=1000)

    def __str__(self):
        return self.cat_name

class CategoryReference(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()

    def get_category_instance(self):
        model_class = globals()[self.category.cat_name]
        return model_class.objects.get(id=self.object_id)

class UserCategories(models.Model):
    user = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE)
    cat = models.ForeignKey(CategoryReference, null=False, on_delete=models.CASCADE)

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    ]

    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPE_CHOICES, default='Debit')
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Amount of the transaction")
    date = models.DateField(help_text="Date of the transaction") 
    description = models.TextField(blank=True, help_text="Detailed description of the transaction")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the record was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="Timestamp when the record was last updated")

class TrackIncomeExpense(Category):
    category = models.CharField(max_length=50, help_text="Category of the transaction (e.g., Salary, Food, Rent)")
    transaction = models.ForeignKey(Transaction, null=False, on_delete=models.CASCADE)
    curr_bal = models.DecimalField(max_digits=12, decimal_places=2, help_text="Total Balance till date")

class BudgetPlan(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the budget plan")
    total_budget = models.DecimalField(max_digits=12, decimal_places=2, help_text="Total budget allocated for the plan")
    amount_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, help_text="Total amount spent so far in this budget plan")
    amount_remaining = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, help_text="Amount remaining in the budget plan")
    transactions = models.ManyToManyField(Transaction, related_name='budget_plans', blank=True)

    def save(self, *args, **kwargs):
        # Calculate the amount spent from associated transactions
        self.amount_spent = self.transactions.filter(transaction_type='debit').aggregate(total_spent=models.Sum('amount'))['total_spent'] or 0.00
        self.amount_remaining = self.total_budget - self.amount_spent
        super().save(*args, **kwargs)