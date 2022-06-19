from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


class Tag(models.Model):
    title = models.CharField(max_length=200, unique=True)


class Snippet(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        get_user_model(),
        related_name="user_snippets",
        on_delete=models.CASCADE,
    )
    tag = models.ForeignKey(
        Tag,
        related_name="snippet_tag",
        on_delete=models.RESTRICT,
    )
