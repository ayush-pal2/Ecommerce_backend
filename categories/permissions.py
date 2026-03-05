from rest_framework.permissions import BasePermission
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

class IsAdmin(BasePermission):
    message = "only admin can access This "
    def has_permission(self, request, view):
        
        if not request.user.is_authenticated:
            logger.warning("Unauthenticated user tried to access admin endpoint")
            return False

        if request.user.role != "admin":
            logger.warning(f"Unauthorized access by user {request.user.id}")
            return False

        return True
    
