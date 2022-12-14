# Generated by Django 4.1.1 on 2022-10-03 16:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0002_budget_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='made_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='transaction',
            name='title',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
