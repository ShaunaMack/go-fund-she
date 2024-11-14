from rest_framework import permissions

class IsSuperUser(permissions.BasePermission):
    #Custom permissions to ensure SuperUsers can view all User List and User Detail content
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_superuser
    
class IsOwnerOrSuperUser(permissions.BasePermission):
    #Custom permissions to allow only the user themselves or a SuperUser to view/edit User Details
    def has_object_permission(self, request, view, obj):
        return request.user == obj or request.user.is_superuser
    