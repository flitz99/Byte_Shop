# Generated by Django 4.0.5 on 2023-04-04 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_ordine_total_price_alter_computer_battery_autonomy_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='num_visits',
        ),
    ]
