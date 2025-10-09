from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners (authors) to edit/delete.
    """

    def has_permission(self, request, view):
        # Allow any user to list or retrieve; only authenticated users create/update/delete
        if view.action in ['list', 'retrieve']:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Read permissions allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only for the owner
        return getattr(obj, 'author', None) == request.user
