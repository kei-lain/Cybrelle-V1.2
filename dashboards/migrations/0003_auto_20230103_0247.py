# Generated by Django 3.2.8 on 2023-01-03 02:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0002_auto_20230102_0222'),
        ('dashboards', '0002_cve'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cve',
            name='CVE',
        ),
        migrations.AddField(
            model_name='cve',
            name='Organization',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.organization'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cve',
            name='user',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
    ]