# Generated by Django 4.0.5 on 2022-06-06 17:20

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('levels', models.PositiveIntegerField()),
                ('order_status', models.IntegerField(choices=[(0, 'Cancelled'), (1, 'Order Confirmed')], default=1)),
                ('order_date', models.DateField(default=datetime.date.today)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.student')),
            ],
        ),
    ]
