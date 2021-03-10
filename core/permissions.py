from rest_framework import permissions

from core.enums import RoleEnum

SAFE_ACTIONS = (
    'get', 'retrieve', 'list', 'head', 'options'
)
class IsAdminOrReadOnly(permissions.IsAuthenticated):
    def permission_analyzer(self, request, view, obj=None):
        try:
            profile = getattr(request.user, 'user_profile', None)
            if profile:
                if profile.role.type != RoleEnum.Admin.value:
                    if view.action in SAFE_ACTIONS:
                        return True
                    return False
                return True
            elif getattr(request.user, 'author', None):
                if view.action in SAFE_ACTIONS:
                    return True
                return False
            return False
        except Exception:
            return False


    def has_permission(self, request, view):
        return self.permission_analyzer(request=request, view=view)

    def has_object_permission(self, request, view, obj):
        return self.permission_analyzer(request=request, view=view, obj=obj)
