from django.db import models


class MOOSEMeta(models.Model):
    oss_id = models.BigIntegerField(unique=True)
    oss_from = models.IntegerField()
    oss_name = models.CharField(max_length=50)
    oss_fullname = models.CharField(max_length=100, unique=True)
    oss_create_time = models.CharField(max_length=50)
    oss_git_url = models.CharField(max_length=200)
    oss_git_tool = models.CharField(max_length=30)
    oss_repo_url = models.CharField(max_length=200)
    oss_homepage = models.CharField(max_length=100)
    oss_license = models.CharField(max_length=100)
    oss_description = models.TextField()
    oss_local_path = models.CharField(max_length=50)
    oss_line_count = models.IntegerField()
    oss_developer_count = models.IntegerField()
    oss_file_count = models.IntegerField()
    oss_commit_count = models.IntegerField()
    oss_lastupdate_time = models.CharField(max_length=50)
    oss_owner_id = models.IntegerField()
    oss_owner_type = models.CharField(max_length=100)
    oss_fork = models.IntegerField()
    oss_star = models.IntegerField()
    oss_main_language = models.CharField(max_length=50)
    oss_owner_id = models.IntegerField()
    oss_owner_type = models.CharField(max_length=11)
    oss_size = models.IntegerField()
    oss_lastupdate_time = models.CharField(max_length=50)
    has_wiki = models.IntegerField()
    readme = models.CharField(max_length=5000)
    uid = models.IntegerField()
    status = models.IntegerField()
    update_time = models.CharField(max_length=50)
    oss_all_day = models.IntegerField()
    oss_active_day = models.IntegerField()
    oss_language = models.CharField(max_length=1000)
    f1 = models.FloatField()
    f2 = models.FloatField()
    f3 = models.FloatField()
    f4 = models.FloatField()
    f5 = models.FloatField()
    f6 = models.FloatField()
    score = models.FloatField()
    def __str__(self):
        return self.oss_fullname

    class Meta:
        db_table = 'moose_metadata'