# Generated by Django 5.0.4 on 2024-04-06 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0003_alter_cost_fellow_alter_costpayment_account_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cost',
            name='months',
            field=models.IntegerField(default=1, verbose_name='На сколько месяцев?'),
        ),
    ]
