from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
     Разрешение для владельца задачи.
     """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsModerator(BasePermission):
    """
    Разрешение для пользователей с правами модератора.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True
        if request.user.groups.filter(name='moderator').exists():
            return True
        return False
