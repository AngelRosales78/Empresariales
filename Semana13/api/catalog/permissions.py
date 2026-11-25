from rest_framework.permissions import SAFE_METHODS

from quiz.permissions import AgentPermission


class CatalogPermission(AgentPermission):
    """Anybody can browse the store; the role decides who may change it."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or super().has_permission(request, view)
