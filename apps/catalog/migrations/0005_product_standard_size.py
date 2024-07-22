# Generated by Django 5.0.3 on 2024-05-02 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_alter_product_section'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='standard_size',
            field=models.CharField(blank=True, choices=[('L1', 'L1'), ('LB1', 'LB1'), ('L2', 'L2'), ('LB2', 'LB2'), ('L3', 'L3'), ('LB3', 'LB3'), ('L4', 'L4'), ('LB4', 'LB4'), ('L5', 'L5'), ('LB5', 'LB5'), ('L6', 'L6'), ('B19', 'B19'), ('B24', 'B24'), ('D23', 'D23'), ('D24', 'D24'), ('D31', 'D31')], max_length=16, null=True, verbose_name='Типоразмер'),
        ),
    ]
