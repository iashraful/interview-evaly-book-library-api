import os

import markdown
from django.conf import settings
from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_404_NOT_FOUND, \
    HTTP_204_NO_CONTENT
from rest_framework.viewsets import ModelViewSet

from core.models import Role, UserProfile
from core.permissions import IsAdminOrReadOnly
from core.serializers import UserRegistrationSerializer, LoginUserSerializer, RoleSerializer


def index(request):
    context = {}
    with open(os.path.join(settings.BASE_DIR, 'README.md')) as readme:
        context['html_readme'] = markdown.markdown(readme.read())
    return render(request, 'index.html', context)


class UserRegistrationViewset(ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=HTTP_201_CREATED)
        return Response(data={'success': False}, status=HTTP_400_BAD_REQUEST)


class LoginUserViewset(ModelViewSet):
    serializer_class = LoginUserSerializer
    parser_classes = (MultiPartParser, FormParser)

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        if user and user.user_profile:
            serializer = LoginUserSerializer(user.user_profile)
            return Response(serializer.data, status=HTTP_200_OK)
        return Response({'message': 'User is not logged in.'}, status=HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        data = request.data
        try:
            instance = UserProfile.objects.get(pk=data['id'])
            serializer = LoginUserSerializer(instance=instance, data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(data=serializer.data, status=HTTP_200_OK)
            return Response(data={'success': False}, status=HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(data={
                'success': False,
                'message': error.__str__()
            }, status=HTTP_400_BAD_REQUEST)


class RoleViewset(ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdminOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        try:
            _object = Role.objects.get(pk=kwargs.get('pk'))
            serializer = RoleSerializer(instance=_object)
            return Response(data=serializer.data, status=HTTP_200_OK)
        except Role.DoesNotExist as err:
            return Response(data={'message': err.__str__()}, status=HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=HTTP_201_CREATED)
        return Response(data=serializer.data, status=HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            _object = Role.objects.get(pk=kwargs.get('pk'))
        except Role.DoesNotExist as err:
            return Response(data={'message': err.__str__()}, status=HTTP_404_NOT_FOUND)
        serializer = RoleSerializer(data=request.data, instance=_object)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=HTTP_200_OK)
        return Response(data=serializer.data, status=HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            Role.objects.get(pk=kwargs.get('pk')).delete()
            return Response(status=HTTP_204_NO_CONTENT)
        except Role.DoesNotExist as err:
            return Response(data={'message': err.__str__()}, status=HTTP_404_NOT_FOUND)
