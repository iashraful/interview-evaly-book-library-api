from django.urls import path

from core.views import UserRegistrationViewset, LoginUserViewset, RoleViewset

urlpatterns = [
    path('user-registration/', UserRegistrationViewset.as_view({'post': 'create'}), name='user_registration'),
    path('me/', LoginUserViewset.as_view({'get': 'retrieve', 'put': 'update'}), name='login_user'),
    path('roles/', RoleViewset.as_view({'get': 'list', 'post': 'create'}), name='roles'),
    path('roles/<int:pk>/', RoleViewset.as_view({'get': 'retrieve', 'put': 'update'}), name='role_details'),
]
