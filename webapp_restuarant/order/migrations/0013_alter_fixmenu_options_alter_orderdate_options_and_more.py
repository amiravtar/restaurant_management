# Generated by Django 4.0.6 on 2022-08-18 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0005_alter_restaurant_admin'),
        ('user', '0004_alter_profile_temp_order'),
        ('food', '0002_initial'),
        ('order', '0012_order_meal_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fixmenu',
            options={},
        ),
        migrations.AlterModelOptions(
            name='orderdate',
            options={},
        ),
        migrations.AlterField(
            model_name='fixmenu',
            name='foods',
            field=models.ManyToManyField(to='food.food'),
        ),
        migrations.AlterField(
            model_name='fixmenu',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='fixmenu',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.restaurant'),
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.CharField(blank=True, max_length=70, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='foods',
            field=models.ManyToManyField(blank=True, to='order.foodcount'),
        ),
        migrations.AlterField(
            model_name='order',
            name='meal_type',
            field=models.CharField(choices=[('dinner', 'ناهار'), ('lunch', 'شام')], default='dinner', max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='order.orderdate'),
        ),
        migrations.AlterField(
            model_name='order',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='restaurant.restaurant'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('temp', 'موقت'), ('pending_confirm', 'در انتظار تایید'), ('confirmed', 'سفارش پذیرفته شده'), ('in_progress', 'در حال آماده سازی'), ('delivery', 'تحویل به پیک'), ('delivered', 'تحویل داده شده به مشتری'), ('failed', 'به مشکل برخورده'), ('not_confirmed', 'تایید نشده')], default='temp', max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='target_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user'),
        ),
        migrations.AlterField(
            model_name='orderdate',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='orderdate',
            name='disable',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='orderdate',
            name='fix_menu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='order.fixmenu'),
        ),
        migrations.AlterField(
            model_name='orderdate',
            name='foods',
            field=models.ManyToManyField(blank=True, related_name='order_date', to='order.datefoodcount'),
        ),
        migrations.AlterField(
            model_name='orderdate',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.restaurant'),
        ),
    ]
