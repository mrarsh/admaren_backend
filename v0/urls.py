from django.urls import include
from django.urls import re_path
from rest_framework import routers
from v0 import views

app_name = "v0"

router = routers.SimpleRouter(trailing_slash=False)
router.register("snippet", views.SnippetViewSet, basename="snippet")
router.register("tag", views.TagViewSet, basename="tag")

urlpatterns = [
    re_path(r"^", include(router.urls)),
]
