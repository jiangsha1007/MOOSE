from django.db import models
from model.oss import *

class MOOSECommunity(models.Model):
    user_id = models.IntegerField()
    community_name = models.CharField(max_length=256)
    create_time = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField()
    class Meta:
        db_table = 'moose_community'


class MOOSECommunityList(models.Model):
    community_id = models.IntegerField()
    oss_id = models.IntegerField()
    oss_name = models.CharField(max_length=256)
    add_time = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField()
    meta_id = models.IntegerField()
    class Meta:
        db_table = 'moose_community_list'