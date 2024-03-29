# Generated by Django 4.0.6 on 2022-08-10 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0003_alter_restaurant_deliver_fee'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='max_reserve_time',
            field=models.SmallIntegerField(default=7),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='tax_delivery',
            field=models.SmallIntegerField(default=0, verbose_name='مالیات بر پیک'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='tax_fix',
            field=models.IntegerField(default=0, verbose_name='مالیات ثابت'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='tax_food',
            field=models.SmallIntegerField(default=0, verbose_name='مالیات بر غذا'),
        ),
    ]
