from rest_framework import serializers

from local_data.models import MusicModel, PlaylistModel


# https://www.django-rest-framework.org/api-guide/serializers/#specifying-which-fields-to-include
class MusicForClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicModel
        exclude = ["path"]


class MusicForServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicModel
        fields = "__all__"


class PlaylistModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaylistModel
        fields = "__all__"
