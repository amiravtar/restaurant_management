# Generated by Django 4.0.6 on 2022-08-11 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_profile_temp_order'),
        ('restaurant', '0004_restaurant_max_reserve_time_restaurant_tax_delivery_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='admin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user', verbose_name='مدیر'),
        ),
    ]
