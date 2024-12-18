# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('SlmsappCustomuser', models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class SlmsappCustomuser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    user_type = models.CharField(max_length=50)
    profile_pic = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'slmsapp_customuser'


class SlmsappCustomuserGroups(models.Model):
    customuser = models.ForeignKey(SlmsappCustomuser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'slmsapp_customuser_groups'
        unique_together = (('customuser', 'group'),)


class SlmsappCustomuserUserPermissions(models.Model):
    customuser = models.ForeignKey(SlmsappCustomuser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'slmsapp_customuser_user_permissions'
        unique_together = (('customuser', 'permission'),)


class SlmsappStaff(models.Model):
    address = models.TextField()
    gender = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    admin = models.OneToOneField(SlmsappCustomuser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'slmsapp_staff'


class SlmsappStaffLeave(models.Model):
    leave_type = models.CharField(max_length=100)
    from_date = models.CharField(max_length=100)
    to_date = models.CharField(max_length=100)
    message = models.TextField()
    status = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    staff_id = models.ForeignKey(SlmsappStaff, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'slmsapp_staff_leave'
