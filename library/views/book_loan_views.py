from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from library.models import BookLoan
from library.serializers import BookLoanSerializer


class BookLoanViewset(ModelViewSet):
    queryset = BookLoan.objects.select_related('request_by', 'approved_by').all()
    serializer_class = BookLoanSerializer

    def create(self, request, *args, **kwargs):
        serializer = BookLoanSerializer(data=self.request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        try:
            _object = BookLoan.objects.get(pk=kwargs.get('pk'))
            serializer = BookLoanSerializer(instance=_object)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except BookLoan.DoesNotExist as err:
            return Response(data={'message': err.__str__()}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        try:
            _object = BookLoan.objects.get(pk=kwargs.get('pk'))
        except BookLoan.DoesNotExist as err:
            return Response(data={'message': err.__str__()}, status=status.HTTP_404_NOT_FOUND)
        serializer = BookLoanSerializer(data=self.request.data, instance=_object)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            BookLoan.objects.get(pk=kwargs.get('pk')).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except BookLoan.DoesNotExist as err:
            return Response(data={'message': err.__str__()}, status=status.HTTP_404_NOT_FOUND)


