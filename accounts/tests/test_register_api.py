from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from accounts.serializers import RegisterSerializer
import logging

User = get_user_model()

class RegisterAPITestCase(APITestCase):
    def setUp(self):
        # Clear the User table before each test to avoid conflicts
        User.objects.all().delete()
        # Disable logging during tests to reduce noise
        logging.disable(logging.CRITICAL)
        self.url = reverse('accounts:register_user')

    def test_successful_registration(self):
        """Test successful user registration with valid data."""
        data = {
            'email': 'testuser@example.com',
            'username': 'testuser',
            'password1': 'Test1234',
            'password2': 'Test1234'
        }
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user']['email'], 'testuser@example.com')
        self.assertEqual(response.data['user']['username'], 'testuser')
        self.assertEqual(response.data['message'], 'User registered successfully')
        
        # Verify user exists in the database
        user = User.objects.get(email='testuser@example.com')
        self.assertTrue(user.check_password('Test1234'))
        self.assertTrue(user.is_active)

    def test_password_mismatch(self):
        """Test registration with mismatched passwords."""
        data = {
            'email': 'testuser@example.com',
            'username': 'testuser',
            'password1': 'Test1234',
            'password2': 'Different1234'
        }
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Passwords do not match', str(response.data['error']))
        self.assertFalse(response.data['success'])

    def test_invalid_email_format(self):
        """Test registration with invalid email format."""
        data = {
            'email': 'invalid-email',
            'username': 'testuser',
            'password1': 'Test1234',
            'password2': 'Test1234'
        }
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid email format', str(response.data['error']))
        self.assertFalse(response.data['success'])

    def test_duplicate_email(self):
        """Test registration with an already existing email."""
        # Create a user first
        User.objects.create_user(email='testuser@example.com', username='existing', password='Test1234')
        
        data = {
            'email': 'testuser@example.com',
            'username': 'newuser',
            'password1': 'Test1234',
            'password2': 'Test1234'
        }
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email already exists', str(response.data['error']))
        self.assertFalse(response.data['success'])

    def test_weak_password(self):
        """Test registration with a weak password (no letters or numbers)."""
        data = {
            'email': 'testuser@example.com',
            'username': 'testuser',
            'password1': '12345678',
            'password2': '12345678'
        }
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Password must contain both letters and numbers', str(response.data['error']))
        self.assertFalse(response.data['success'])

    def test_missing_required_fields(self):
        """Test registration with missing required fields."""
        
        data = {
            'username': 'testuser',
            'password1': 'Test1234',
            'password2': 'Test1234'
        }
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', str(response.data['error']))
        self.assertFalse(response.data['success'])

    def test_serializer_validation(self):
        """Test RegisterSerializer validation directly."""
        data = {
            'email': 'testuser@example.com',
            'username': 'testuser',
            'password1': 'Test1234',
            'password2': 'Test1234'
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        user = serializer.save()
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertTrue(user.check_password('Test1234'))

    def test_serializer_invalid_data(self):
        """Test RegisterSerializer with invalid data."""
        data = {
            'email': 'invalid-email',
            'username': 'testuser',
            'password1': 'Test1234',
            'password2': 'Test1234'
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('Invalid email format', str(serializer.errors))

    def test_serializer_valid_email(self):
        """Test RegisterSerializer with a valid email format."""
        data = {
            'email': 'validuser@example.com',
            'username': 'validuser',
            'password1': 'Test1234',
            'password2': 'Test1234'
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid(), f"Serializer errors: {serializer.errors}")
        self.assertEqual(serializer.validated_data['email'], 'validuser@example.com')

    def test_user_model_creation(self):
        """Test User model creation via UserManager."""
        user = User.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='Test1234'
        )
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertTrue(user.check_password('Test1234'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def tearDown(self):
        # Re-enable logging after tests
        logging.disable(logging.NOTSET)
