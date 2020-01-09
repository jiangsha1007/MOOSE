from rest_framework import serializers
from model import oss

class Serializer(serializers.ModelSerializer):
    class Meta:
        model = oss.MOOSEMeta
        fields = ("oss_id", "oss_name", "oss_fullname")






