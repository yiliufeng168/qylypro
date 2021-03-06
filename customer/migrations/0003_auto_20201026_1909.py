# Generated by Django 3.1.2 on 2020-10-26 19:09

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_auto_20201026_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='id',
            field=models.UUIDField(default=uuid.UUID('7767a8ea-279d-4dc9-80ac-a8f4e9fd93d6'), primary_key=True, serialize=False, verbose_name='订单ID'),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='id',
            field=models.UUIDField(default=uuid.UUID('f81035ea-49d4-44d3-8d62-f14c07b31e08'), primary_key=True, serialize=False, verbose_name='订单详细ID'),
        ),
        migrations.AlterField(
            model_name='tourist',
            name='sessionid',
            field=models.UUIDField(default=uuid.UUID('aaf0d799-63f0-401a-bbe4-493a803bd138'), verbose_name='sessionid'),
        ),
    ]
