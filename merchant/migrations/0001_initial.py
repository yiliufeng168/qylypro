# Generated by Django 3.1.2 on 2020-10-18 15:44

from django.db import migrations, models
import django.db.models.deletion
import merchant.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='management.user', verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='商家名')),
                ('location', models.CharField(max_length=128, verbose_name='地址')),
                ('pic', models.ImageField(blank=True, upload_to=merchant.models.pic_path, verbose_name='图片地址')),
                ('star', models.PositiveIntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=0, verbose_name='星级')),
                ('introduct', models.CharField(max_length=1000, verbose_name='简介')),
                ('score', models.DecimalField(decimal_places=1, default=0, max_digits=2, verbose_name='评分')),
                ('type', models.PositiveIntegerField(choices=[(0, '酒店'), (1, '景区')], default=0, verbose_name='类型')),
            ],
            options={
                'verbose_name': '商户',
                'verbose_name_plural': '商户',
            },
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='商品编号')),
                ('name', models.CharField(max_length=50, verbose_name='商品名')),
                ('pic', models.ImageField(blank=True, upload_to=merchant.models.pic_path, verbose_name='图片地址')),
                ('introduct', models.CharField(max_length=500, null=True, verbose_name='简介')),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='merchant.business', verbose_name='所属商家')),
            ],
        ),
        migrations.CreateModel(
            name='Sell',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.PositiveIntegerField(verbose_name='发售数量')),
                ('surplus', models.PositiveIntegerField(default=models.PositiveIntegerField(verbose_name='发售数量'), verbose_name='剩余数量')),
                ('startdatetime', models.DateTimeField(blank=True, null=True, verbose_name='开始时间')),
                ('enddatetime', models.DateTimeField(blank=True, null=True, verbose_name='结束时间')),
                ('price', models.FloatField(default=999, verbose_name='价格')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='merchant.goods', verbose_name='所指的的商品')),
            ],
        ),
    ]
