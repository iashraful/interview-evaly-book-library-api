from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.viewsets import ModelViewSet

from core.serializers import UserRegistrationSerializer, LoginUserSerializer


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

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        if user and user.user_profile:
            serializer = LoginUserSerializer(user.user_profile)
            return Response(serializer.data, status=HTTP_200_OK)
        return Response({'message': 'User is not logged in.'}, status=HTTP_400_BAD_REQUEST)
