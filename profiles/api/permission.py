import logging
from rest_framework import permissions


class IsOwnerProfileOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user)
        else:
            return request.user.user.id == obj.user.id
