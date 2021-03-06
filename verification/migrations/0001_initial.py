# Generated by Django 3.1.2 on 2020-10-18 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('management', '0001_initial'),
        ('merchant', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vofficer',
            fields=[
                ('vuser', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='management.user', verbose_name='核销员id')),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='merchant.business', verbose_name='商户id')),
            ],
        ),
    ]
