# Generated by Django 4.0.3 on 2022-07-13 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('restaurant', '0001_initial'),
        ('order', '0001_initial'),
        ('deliver', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliver',
            name='driver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.driver'),
        ),
        migrations.AddField(
            model_name='deliver',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deliver', to='order.order'),
        ),
    ]