# Generated by Django 3.1.2 on 2020-10-17 14:45

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_auto_20201017_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='id',
            field=models.UUIDField(default=uuid.UUID('f6fdecfe-ed63-4f43-bd4f-86a1eea7bf9f'), primary_key=True, serialize=False, verbose_name='订单ID'),
        ),
        migrations.AlterField(
            model_name='order',
            name='orderstatus',
            field=models.PositiveIntegerField(choices=[(0, '未发货'), (1, '已发货'), (2, '异常'), (3, '关闭')], default=0, verbose_name='订单状态'),
        ),
        migrations.AlterField(
            model_name='tourist',
            name='sessionid',
            field=models.UUIDField(default=uuid.UUID('6b227b1f-7924-41de-9d5b-a110d0b0a9bf'), verbose_name='sessionid'),
        ),
    ]
