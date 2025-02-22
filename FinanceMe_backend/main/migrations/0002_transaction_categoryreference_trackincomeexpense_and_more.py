# Generated by Django 5.1 on 2024-09-01 05:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('credit', 'Credit'), ('debit', 'Debit')], default='Debit', max_length=7)),
                ('amount', models.DecimalField(decimal_places=2, help_text='Amount of the transaction', max_digits=10)),
                ('date', models.DateField(help_text='Date of the transaction')),
                ('description', models.TextField(blank=True, help_text='Detailed description of the transaction')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp when the record was created')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Timestamp when the record was last updated')),
            ],
        ),
        migrations.CreateModel(
            name='CategoryReference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TrackIncomeExpense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_name', models.CharField(max_length=500, unique=True)),
                ('cat_desc', models.TextField(max_length=1000)),
                ('category', models.CharField(help_text='Category of the transaction (e.g., Salary, Food, Rent)', max_length=50)),
                ('curr_bal', models.DecimalField(decimal_places=2, help_text='Total Balance till date', max_digits=12)),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.transaction')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BudgetPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the budget plan', max_length=100)),
                ('total_budget', models.DecimalField(decimal_places=2, help_text='Total budget allocated for the plan', max_digits=12)),
                ('amount_spent', models.DecimalField(decimal_places=2, default=0.0, help_text='Total amount spent so far in this budget plan', max_digits=12)),
                ('amount_remaining', models.DecimalField(decimal_places=2, default=0.0, help_text='Amount remaining in the budget plan', max_digits=12)),
                ('transactions', models.ManyToManyField(blank=True, related_name='budget_plans', to='main.transaction')),
            ],
        ),
        migrations.CreateModel(
            name='UserCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.categoryreference')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
