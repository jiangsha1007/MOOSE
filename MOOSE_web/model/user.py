from django.db import models


class OsslibAdmin(models.Model):
    user_name = models.CharField(max_length=128, unique=True)
    user_pasword = models.CharField(max_length=256)
    user_email = models.EmailField(unique=True)
    register_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_name

    class Meta:
        ordering = ['register_time']
        db_table = 'osslib_admin'
