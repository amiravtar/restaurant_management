# Generated by Django 4.0.3 on 2022-07-13 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Deliver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('inway', 'در راه'), ('pickup', 'در حال دریافت از رستوران'), ('deliverd', 'تحویل داده شده'), ('ndeliverd', 'تحویل داده نشده')], max_length=20)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
