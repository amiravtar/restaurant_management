# Generated by Django 4.0.6 on 2022-08-10 16:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0010_fixmenu_restaurant'),
        ('user', '0002_profile_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='temp_order',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='order.order'),
        ),
    ]