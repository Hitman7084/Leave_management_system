# Generated by Django 5.1.6 on 2025-03-27 20:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clmsapp', '0003_leaveapplication_delete_leaverequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaveapplication',
            name='forwarded_to_dean',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='leaveapplication',
            name='incharge',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_leaves', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='leaveapplication',
            name='incharge_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='leaveapplication',
            name='rejection_reason',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='leaveapplication',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leave_requests', to=settings.AUTH_USER_MODEL),
        ),
    ]
