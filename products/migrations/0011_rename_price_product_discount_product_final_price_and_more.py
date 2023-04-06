# Generated by Django 4.0.5 on 2023-04-06 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_alter_computer_ram'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='price',
            new_name='discount',
        ),
        migrations.AddField(
            model_name='product',
            name='final_price',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='full_price',
            field=models.FloatField(default=0),
        ),
    ]
