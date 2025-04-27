from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework.serializers import ValidationError
from rest_framework.permissions import IsAuthenticated
from accounts.models import BlacklistedToken
from core.utils import get_logger
logger = get_logger(__name__)
User = get_user_model()



class RegisterView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            # Deserialize and validate input data
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()  # Save the validated user data

                logger.info(f"user logged in!")
                # Success response with user details
                return Response({
                    "user": {
                        "email": user.email,
                        "username": user.username,
                    },
                    "message": "User registered successfully"
                }, status=status.HTTP_201_CREATED)
            
            # If validation fails, raise error with serializer errors
            else:
                raise ValueError(serializer.errors)

        except (ValueError, ValidationError) as error:
            # Log validation errors and return bad request response
            logger.error(error)
            return Response({
                'error': str(error),
                'success': False},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as error:
            # Log any other unexpected exceptions
            logger.exception(f"Exception is :  {error}")
            return Response({
                'error': f"{error}",
                'success': False},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request):
        try:
            # Get the token from the Authorization header
            token = request.headers.get('Authorization', None)
            if token is None or not token.startswith('Bearer '):
                return Response({
                    'error': 'Token not provided',
                    'success': False
                }, status=status.HTTP_400_BAD_REQUEST)

            token = token[7:]  # Remove 'Bearer ' prefix from the token

            # Blacklist the token by storing it in the database
            BlacklistedToken.objects.create(token=token)

            # Return success message
            return Response({
                'message': 'Logged out successfully.',
                'success': True
            }, status=status.HTTP_200_OK)

        except Exception as error:
            # Catch any other errors during the logout process
            return Response({
                'error': str(error),
                'success': False
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
