from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from library.models import Author
from library.serializers import AuthorSerializer


class AuthorViewset(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def create(self, request, *args, **kwargs):
        serializer = AuthorSerializer(data=self.request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        try:
            _object = Author.objects.get(pk=kwargs.get('pk'))
            serializer = AuthorSerializer(instance=_object)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Author.DoesNotExist as err:
            return Response(data={'message': err.__str__()}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        try:
            _object = Author.objects.get(pk=kwargs.get('pk'))
        except Author.DoesNotExist as err:
            return Response(data={'message': err.__str__()}, status=status.HTTP_404_NOT_FOUND)
        serializer = AuthorSerializer(data=self.request.data, instance=_object)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            Author.objects.get(pk=kwargs.get('pk')).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Author.DoesNotExist as err:
            return Response(data={'message': err.__str__()}, status=status.HTTP_404_NOT_FOUND)


