import os
from datetime import datetime

import tablib
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from core.permissions import IsAdminOrReadOnly, IsAdminOrNoAccess
from library.enums import BookLoanStatusEnum
from library.models import BookLoan
from library.serializers import BookLoanSerializer, BookLoanExportSerializer
from django.conf import settings


class BookLoanViewset(ModelViewSet):
    queryset = BookLoan.objects.select_related('book', 'request_by', 'action_taken_by').all()
    serializer_class = BookLoanSerializer
    permission_classes = [IsAdminOrReadOnly]

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


class BookLoanApproveView(ModelViewSet):
    serializer_class = BookLoanSerializer
    permission_classes = [IsAdminOrReadOnly]

    def update(self, request, *args, **kwargs):
        try:
            _object = BookLoan.objects.get(pk=kwargs.get('pk'))
            _object.action_taken_by = request.user.user_profile
            _object.action_date = timezone.now()
            _object.status = BookLoanStatusEnum.Approved.value
            _object.save()
            serializer = BookLoanSerializer(_object)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except BookLoan.DoesNotExist as err:
            return Response(data={'message': err.__str__()}, status=status.HTTP_404_NOT_FOUND)
        except Exception as err:
            return Response(data={'message': err.__str__()}, status=status.HTTP_400_BAD_REQUEST)


class BookLoanRejectView(ModelViewSet):
    serializer_class = BookLoanSerializer
    permission_classes = [IsAdminOrReadOnly]

    def update(self, request, *args, **kwargs):
        try:
            _object = BookLoan.objects.get(pk=kwargs.get('pk'))
            _object.action_taken_by = request.user.user_profile
            _object.action_date = timezone.now()
            _object.status = BookLoanStatusEnum.Rejected.value
            _object.save()
            serializer = BookLoanSerializer(_object)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except BookLoan.DoesNotExist as err:
            return Response(data={'message': err.__str__()}, status=status.HTTP_404_NOT_FOUND)
        except Exception as err:
            return Response(data={'message': err.__str__()}, status=status.HTTP_400_BAD_REQUEST)


class BookLoanExportView(APIView):
    permission_classes = [IsAdminOrNoAccess]

    def render_date_field(self, value, format='%d-%m-%Y %I:%M %p'):
        if isinstance(value, datetime):
            return value.strftime(format)

    def get(self, request, *args, **kwargs):
        try:
            book_loans = BookLoan.objects.select_related('book', 'request_by', 'action_taken_by').values(
                'pk', 'book__title', 'book__author__name', 'request_by__full_name', 'request_by__role__name',
                'action_taken_by__full_name', 'action_taken_by__role__name', 'status',
                'action_date', 'repayment_date', 'created_at',
            )
            _headers = (
                'Book Name', 'Author Name', 'Requested by', 'Role of Requested by', 'Requested Time',
                'Approved/Rejected by', 'Role of Approved/Rejected by', 'Status', 'Approved/Rejected Date',
                'Repayment Date'
            )
            data = tablib.Dataset(headers=_headers)
            for loan in book_loans:
                _row = (
                    loan['book__title'], loan['book__author__name'], loan['request_by__full_name'],
                    loan['request_by__role__name'], self.render_date_field(loan['created_at']),
                    loan['action_taken_by__full_name'],
                    loan['action_taken_by__role__name'], BookLoanStatusEnum(loan['status']).name,
                    self.render_date_field(loan['action_date']), self.render_date_field(loan['repayment_date'])
                )
                data.append(_row)
            _filename = f'Exported_Book_Loans_{int(timezone.now().timestamp() * 1000)}.xlsx'
            if not os.path.exists(settings.EXPORTED_FILES):
                os.makedirs(settings.EXPORTED_FILES)
            _path = os.path.join(settings.EXPORTED_FILES, _filename)
            with open(_path, 'wb') as export_file:
                export_file.write(data.export('xlsx'))
                return Response(
                    data={'path': f'{settings.MEDIA_URL}{settings.EXPORTED_FILES_DIR}/{_filename}'},
                    status=status.HTTP_200_OK)
        except Exception as error:
            return Response(data={'message': error.__str__()}, status=status.HTTP_400_BAD_REQUEST)
