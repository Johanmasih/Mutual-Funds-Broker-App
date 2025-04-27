

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from datetime import datetime
import logging
from rest_framework.serializers import ValidationError as DRFValidationError
def get_logger(name):
    return logging.getLogger(name)


logger = get_logger('funds')

def parse_date(date_str):
    return datetime.strptime(date_str, '%d-%b-%Y').date()



# utils/exception_handler.py
def custom_exception_handler(exc, context):
    # Call DRF default exception handler first
    response = exception_handler(exc, context)

    if response is not None:
        # You can add success: False always
        response.data['success'] = False
        response.data['status_code'] = response.status_code
        logger.error(f"Handled Exception: {exc}")
    else:
        if isinstance(exc, ObjectDoesNotExist):
            logger.warning(f"Object Not Found: {exc}")
            return Response({
                'success': False,
                'error': 'Resource not found.',
            }, status=status.HTTP_404_NOT_FOUND)

        if isinstance(exc, (ValidationError, DRFValidationError)):
            logger.warning(f"Validation Error: {exc}")
            return Response({
                'success': False,
                'error': str(exc),
            }, status=status.HTTP_400_BAD_REQUEST)

        logger.exception(f"Unhandled server error: {exc}")
        return Response({
            'success': False,
            'error': 'Internal server error. Please try again later.',
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response
