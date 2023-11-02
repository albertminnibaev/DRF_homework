from rest_framework.permissions import BasePermission


# пользователь является создателем
class IsCreator(BasePermission):
    message = "Вы не являетесь создателем"

    def has_object_permission(self, request, view, obj):
        if request.user == obj.creator:
            return True
        return False


class IsRetrieveCreator(BasePermission):
    message = "Вы не являетесь создателем"

    def has_permission(self, request, view):
        if request.user == view.get_object().creator:
            return True
        return False
