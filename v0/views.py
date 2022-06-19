from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from v0 import serializers
from v0 import models
from rest_framework import status
from rest_framework.decorators import action

# Create your views here.


class TagViewSet(viewsets.GenericViewSet):
    """ Viewset to list tags and snippet related to individual tag"""
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.TagSnippetSerializer

    def get_queryset(self):
        return models.Tag.objects

    def list(self, request):
        data = serializers.TagSerializer(self.get_queryset(), many=True).data
        return Response(data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        tag_id = self.kwargs.get("pk")
        ins_tag = get_object_or_404(models.Tag, pk=tag_id)
        data = self.get_serializer(ins_tag).data
        return Response(data, status=status.HTTP_200_OK)


class SnippetViewSet(viewsets.ModelViewSet):
    """ CRUD Api for snippet"""

    permission_classes = [IsAuthenticated]
    serializer_class = serializers.SnippetSerializer
    queryset = models.Snippet.objects.all()

    def list(self, request):
        total_count = len(self.get_queryset())
        snippets = [
            {
                "snippet_title": snippet.title,
                "link": f"http://{request.get_host()}{request.get_full_path()}/{snippet.id}",
            }
            for snippet in self.get_queryset()
        ]
        resp = {"total_snippet_count": total_count, "snippets": snippets}
        return Response(resp)

    def create(self, request, *args, **kwargs):
        self.get_serializer(data=request.data).is_valid(True)
        user = request.user
        tag_title = request.data.get("tag")
        snippet_title = request.data.get("title")
        snippet_text = request.data.get("text")
        ins_tag, _ = models.Tag.objects.get_or_create(title=tag_title)
        models.Snippet.objects.create(
            user=user,
            title=snippet_title,
            text=snippet_text,
            tag=ins_tag,
        )
        resp = {"code": 201, "msg": "Snippet created successfully"}
        return Response(resp, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        snippet_id = self.kwargs.get("pk")
        ins_snippet = get_object_or_404(models.Snippet, pk=snippet_id)
        self.get_serializer(data=request.data).is_valid(True)
        tag_title = request.data.get("tag")
        snippet_title = request.data.get("title")
        snippet_text = request.data.get("text")
        ins_tag, _ = models.Tag.objects.get_or_create(title=tag_title)
        ins_snippet.user = request.user
        ins_snippet.title = snippet_title
        ins_snippet.text = snippet_text
        ins_snippet.tag = ins_tag
        ins_snippet.save()
        serializer = self.get_serializer(
            ins_snippet,
        )
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        snippet_id = self.kwargs.get("pk")
        ins_snippet = get_object_or_404(models.Snippet, pk=snippet_id)
        serializer = self.get_serializer(ins_snippet)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        snippet_id = self.kwargs.get("pk")
        ins_snippet = get_object_or_404(models.Snippet, pk=snippet_id)
        ins_snippet.delete()
        serializer = self.get_serializer(models.Snippet.objects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="delete-multiple")
    def delete_multiple(self, request):
        snippet_ids = request.data.get("snippet_ids", [])
        if not snippet_ids:
            raise ParseError(detail="Missing Parameter")
        models.Snippet.objects.filter(id__in=snippet_ids).delete()
        serializer = self.get_serializer(models.Snippet.objects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
