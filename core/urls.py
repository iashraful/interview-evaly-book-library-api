from django.urls import path

from core.views import UserRegistrationViewset, LoginUserViewset

urlpatterns = [
    path('user-registration/', UserRegistrationViewset.as_view({'post': 'create'}), name='user_registration'),
    path('me/', LoginUserViewset.as_view({'get': 'retrieve'}), name='login_user')
]
