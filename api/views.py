import os.path as osp

from django.http import FileResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from local_data.models import MusicModel, PlaylistModel

from .serializers import (
    MusicForClientSerializer,
    MusicForServerSerializer,
    PlaylistModelSerializer,
)


@api_view(["GET", "POST"])
def music_list(request: Request):
    match request.method:
        case "GET":
            objs = MusicModel.objects.all()
            serializer = MusicForClientSerializer(objs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        case "POST":
            serializer = MusicForServerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def music_detail(request: Request, id: int):
    try:
        obj = MusicModel.objects.get(id=id)
    except MusicModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    match request.method:
        case "GET":
            serializer = MusicForClientSerializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        case "PUT":
            serializer = MusicForServerSerializer(obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        case "DELETE":
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
def playlist_list(request: Request):
    match request.method:
        case "GET":
            objs = PlaylistModel.objects.all()
            serializer = PlaylistModelSerializer(objs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        case "POST":
            serializer = PlaylistModelSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def playlist_detail(request: Request, id: int):
    try:
        obj = PlaylistModel.objects.get(id=id)
    except PlaylistModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    match request.method:
        case "GET":
            serializer = PlaylistModelSerializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        case "PUT":
            serializer = PlaylistModelSerializer(obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        case "DELETE":
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def music_file(request: Request, id: int):
    try:
        obj = MusicModel.objects.get(id=id)
    except MusicModel.DoesNotExist:
        return Response(
            {"msg": f"no data found: {id}"}, status=status.HTTP_404_NOT_FOUND
        )

    if not osp.exists(obj.path):
        return Response(
            {"msg": f"no file found: {obj.path}"}, status=status.HTTP_404_NOT_FOUND
        )

    response = FileResponse(open(obj.path, "rb"))
    _, ext = osp.splitext(obj.path)
    mime = {".mp3": "mpeg", ".flac": "flac"}.get(ext, "mpeg")
    response["Content-Type"] = f"audio/{mime}"
    # 可拖动进度条的关键
    response["Accept-Ranges"] = "bytes"
    return response
