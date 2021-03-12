from rest_condition import Or
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.permissions import IsAdminOrReadOnly, AllowAuthorUserReadAccess
from library.models import Book
from library.serializers import BookSerializer


class BookViewset(ModelViewSet):
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [Or(AllowAuthorUserReadAccess, IsAdminOrReadOnly)]

    def create(self, request, *args, **kwargs):
        serializer = BookSerializer(data=self.request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        try:
            _object = Book.objects.get(pk=kwargs.get('pk'))
            serializer = BookSerializer(instance=_object)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Book.DoesNotExist as err:
            return Response(data={'message': err.__str__()}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        try:
            _object = Book.objects.get(pk=kwargs.get('pk'))
        except Book.DoesNotExist as err:
            return Response(data={'message': err.__str__()}, status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(data=self.request.data, instance=_object)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            Book.objects.get(pk=kwargs.get('pk')).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Book.DoesNotExist as err:
            return Response(data={'message': err.__str__()}, status=status.HTTP_404_NOT_FOUND)


