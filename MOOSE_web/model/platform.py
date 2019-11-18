from django.db import models


class OsslibPlatform(models.Model):
    platform_name = models.CharField(max_length=256)
    get_oss_list_api = models.CharField(max_length=500)
    get_oss_single_api = models.CharField(max_length=500)
    git_api = models.CharField(max_length=500)
    class Meta:
        db_table = 'osslib_platform_api'