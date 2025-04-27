# utils/exception_handler.py

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework.exceptions import AuthenticationFailed
from core.utils import get_logger
logger = get_logger('funds')



from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError, ObjectDoesNotExist as DRFObjectDoesNotExist
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
import logging

# Get the logger
logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    # Call DRF's default exception handler first
    response = exception_handler(exc, context)

    if response is not None:
        # Modify response if it was already handled by DRF's default handler
        response.data['success'] = False
        response.data['status_code'] = response.status_code
        logger.error(f"Handled Exception: {exc}")
    else:
        # If exception wasn't handled by DRF, handle specific known exceptions

        # Handle ObjectDoesNotExist (404 error)
        if isinstance(exc, (ObjectDoesNotExist, DRFObjectDoesNotExist)):
            logger.warning(f"Object Not Found: {exc}")
            return Response({
                'success': False,
                'error': 'Resource not found.',
                'status_code': status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)

        # Handle ValidationError (400 error)
        if isinstance(exc, ValidationError):
            logger.warning(f"Validation Error: {exc}")
            return Response({
                'success': False,
                'error': str(exc),
                'status_code': status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

        # Handle AuthenticationFailed (401 error)
        if isinstance(exc, AuthenticationFailed):
            logger.warning(f"Authentication Failed: {exc}")
            return Response({
                'success': False,
                'error': 'Authentication credentials were not provided.',
                'status_code': status.HTTP_401_UNAUTHORIZED
            }, status=status.HTTP_401_UNAUTHORIZED)

        # Handle PermissionDenied (403 error)
        if isinstance(exc, PermissionDenied):
            logger.warning(f"Permission Denied: {exc}")
            return Response({
                'success': False,
                'error': 'You do not have permission to perform this action.',
                'status_code': status.HTTP_403_FORBIDDEN
            }, status=status.HTTP_403_FORBIDDEN)

        # If the exception is not caught, return a 500 server error
        logger.exception(f"Unhandled server error: {exc}")
        return Response({
            'success': False,
            'error': 'Internal server error. Please try again later.',
            'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response
