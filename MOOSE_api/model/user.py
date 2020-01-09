from django.db import models


class UserInfo(models.Model):
    USER_TYPE = (
        (1, '普通用户'),
        (2, 'VIP'),
        (3, 'SVIP')
    )

    user_type = models.IntegerField(choices=USER_TYPE, default=1)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)

    class Meta:
        db_table = 'moose_api_admin'


class UserToken(models.Model):
    user = models.OneToOneField(UserInfo, on_delete=models.CASCADE)
    token = models.CharField(max_length=64)

    class Meta:
        db_table = 'moose_api_admin_token'