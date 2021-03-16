# Generated by Django 3.1.2 on 2020-12-08 02:07

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_auto_20201207_1901'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='image',
            new_name='student_image',
        ),
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(default=datetime.datetime(2020, 12, 8, 2, 7, 0, 55916, tzinfo=utc)),
        ),
    ]
