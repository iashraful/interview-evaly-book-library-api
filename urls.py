from django.urls import include, path

from rest_framework.permissions import AllowAny
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import (obtain_jwt_token, refresh_jwt_token,
                                      verify_jwt_token)

urlpatterns = []

urlpatterns += [
    path('', include_docs_urls(
        title='Library Management System API Docs', permission_classes=[AllowAny]
    )),
    path('api/', include('core.urls')),
    path('api/', include('library.urls')),
    path('api/jwt-token/', obtain_jwt_token),
    path('api/jwt-refresh/', refresh_jwt_token),
    path('api/jwt-verify/', verify_jwt_token)
]
