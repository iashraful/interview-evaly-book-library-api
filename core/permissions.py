from rest_framework import permissions

from core.enums import RoleEnum

SAFE_ACTIONS = (
    # The whole project I have used some actions. Where the following actions are for SAFE methods.
    'get', 'retrieve', 'list', 'head', 'options'
)

GET_OR_CREATE_ACTIONS = (
    'get', 'retrieve', 'list', 'head', 'options',
    'create', 'post'
)


class IsMemberCreateAccess(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        try:
            profile = getattr(request.user, 'user_profile', None)
            if profile:
                if profile.role.type == RoleEnum.Member.value:
                    if view.action in GET_OR_CREATE_ACTIONS:
                        return True
                    return False
                return False
            return False
        except Exception:
            return False


class IsAdminOrReadOnly(permissions.IsAuthenticated):
    '''
    THe permission class have the power to control every request and decide on response.
    '''

    def permission_analyzer(self, request, view, obj=None):
        try:
            # We have already One2One relation with User model and User Profile model
            # Django put User model instance on request. So, I just need to check the user_profile and roll on it.
            profile = getattr(request.user, 'user_profile', None)
            if profile:
                # If the profile is not admin then it has only safe action permissions. For example,
                # Only can create, update, delete any object rather non admin user has readonly access.
                if profile.role.type != RoleEnum.Admin.value:
                    if view.action in SAFE_ACTIONS:
                        return True
                    return False
                # If the user is admin then it should be YES/True
                return True
            return False
        except Exception:
            return False

    def has_permission(self, request, view):
        return self.permission_analyzer(request=request, view=view)

    def has_object_permission(self, request, view, obj):
        return self.permission_analyzer(request=request, view=view, obj=obj)


class AllowAuthorUserReadAccess(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        # This is another special permission for author user only.
        # Who can
        if getattr(request.user, 'author', None):
            if view.action in SAFE_ACTIONS:
                return True
            return False
        return False


class IsAdminOrNoAccess(permissions.IsAuthenticated):
    '''
    For some of the views who have only admin access.
    '''

    def has_permission(self, request, view):
        try:
            profile = getattr(request.user, 'user_profile', None)
            if profile:
                if profile.role.type == RoleEnum.Admin.value:
                    return True
                return False
            return False
        except Exception:
            return False

    def has_object_permission(self, request, view, obj):
        try:
            profile = getattr(request.user, 'user_profile', None)
            if profile:
                if profile.role.type == RoleEnum.Admin.value:
                    return True
                return False
            return False
        except Exception:
            return False
