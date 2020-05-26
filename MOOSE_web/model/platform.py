from django.db import models


class MOOSEPlatform(models.Model):
    platform_name = models.CharField(max_length=256)
    get_oss_list_api = models.CharField(max_length=500)
    get_oss_single_api = models.CharField(max_length=500)
    git_api = models.CharField(max_length=500)
    refresh_code = models.CharField(max_length=500)
    access_token = models.CharField(max_length=500)
    class Meta:
        db_table = 'moose_platform_api'