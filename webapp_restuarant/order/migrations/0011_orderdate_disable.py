# Generated by Django 4.0.6 on 2022-08-10 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0010_fixmenu_restaurant'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdate',
            name='disable',
            field=models.BooleanField(default=False, verbose_name='غیر فعال'),
        ),
    ]
