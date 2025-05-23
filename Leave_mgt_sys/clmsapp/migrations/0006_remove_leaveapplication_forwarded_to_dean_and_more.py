# Generated by Django 5.1.6 on 2025-03-28 19:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clmsapp', '0005_alter_leaveapplication_incharge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leaveapplication',
            name='forwarded_to_dean',
        ),
        migrations.RemoveField(
            model_name='leaveapplication',
            name='incharge_approved',
        ),
        migrations.AddField(
            model_name='leaveapplication',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10),
        ),
        migrations.AlterField(
            model_name='leaveapplication',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to='leave_attachments/'),
        ),
        migrations.AlterField(
            model_name='leaveapplication',
            name='incharge',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='incharge_requests', to=settings.AUTH_USER_MODEL),
        ),
    ]
