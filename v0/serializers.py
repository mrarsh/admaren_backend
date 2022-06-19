from rest_framework import serializers
from v0 import models


class SnippetSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200, required=True)
    text = serializers.CharField(required=True)
    created = serializers.DateTimeField(required=False, format="%Y-%m-%d %H:%M:%S")
    tag = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username

    def get_tag(self, obj):
        return obj.tag.title


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = "__all__"


class LinkedSnippetSerializer(serializers.Serializer):
    title = serializers.CharField()
    text = serializers.CharField()
    user = serializers.SerializerMethodField()
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    def get_user(self, obj):
        return obj.user.username


class TagSnippetSerializer(serializers.Serializer):
    tag = serializers.SerializerMethodField("tag_title")
    linked_snippets = serializers.SerializerMethodField()

    def tag_title(self, obj):
        return obj.title

    def get_linked_snippets(self, obj):
        snippets = models.Snippet.objects.filter(tag=obj)
        return LinkedSnippetSerializer(snippets, many=True).data
