from django.db import models
from model.oss import *

class OsslibCommunity(models.Model):
    user_id = models.IntegerField()
    community_name = models.CharField(max_length=256)
    create_time = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField()
    class Meta:
        db_table = 'osslib_community'


class OsslibCommunityList(models.Model):
    community_id = models.IntegerField()
    oss_id = models.IntegerField()
    oss_name = models.CharField(max_length=256)
    add_time = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField()
    meta_id = models.IntegerField()
    class Meta:
        db_table = 'osslib_community_list'