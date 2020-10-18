# Generated by Django 3.1.2 on 2020-10-18 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
        ('verification', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vofficer',
            name='id',
        ),
        migrations.RemoveField(
            model_name='vofficer',
            name='vuer',
        ),
        migrations.AddField(
            model_name='vofficer',
            name='vuser',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='management.user', verbose_name='核销员id'),
            preserve_default=False,
        ),
    ]
