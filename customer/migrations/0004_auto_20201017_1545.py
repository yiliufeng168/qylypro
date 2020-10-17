# Generated by Django 3.1.2 on 2020-10-17 15:45

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_auto_20201017_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='id',
            field=models.UUIDField(default=uuid.UUID('9f0608c3-73a2-452a-83c1-ce832a19ba79'), primary_key=True, serialize=False, verbose_name='订单ID'),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='id',
            field=models.UUIDField(default=uuid.UUID('096c7bf9-c30c-42f1-8ca0-6065ee15e9f2'), primary_key=True, serialize=False, verbose_name='订单详细ID'),
        ),
        migrations.AlterField(
            model_name='tourist',
            name='sessionid',
            field=models.UUIDField(default=uuid.UUID('6cdfa9db-2ddd-42fd-b702-56bde84fca99'), verbose_name='sessionid'),
        ),
    ]
