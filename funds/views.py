from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.serializers import ValidationError as DRFValidationError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .models import FundFamily, MutualFund, Portfolio
from .serializers import FundFamilySerializer, MutualFundSerializer, PortfolioSerializer
import requests
from core.utils import parse_date  # Utility function for parsing dates
from core.utils import get_logger  # Logger utility for tracking events
import os

# Initialize logger for this module. All log statements will be tagged under 'funds'.
logger = get_logger('funds')

class FundFamilyListView(APIView):
    """
    API View to handle the listing of all Fund Families.
    This view requires the user to be authenticated.
    """
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can access this view

class FundFamilyListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
           # Validate query parameters (handle invalid page_size)
            page_size = request.query_params.get('page_size', '10')
            
            # Check if page_size is valid; if not, fallback to the default value (10)
            if not page_size.isdigit() or int(page_size) <= 0:
                page_size = 10  
            
            # Order the queryset to avoid the warning
            families = FundFamily.objects.all().order_by('id')

            # Set up Pagination
            paginator = PageNumberPagination()
            paginator.page_size = int(page_size)  # Dynamically setting page size from query parameter
            
            # Paginate the queryset (FundFamily objects)
            result_page = paginator.paginate_queryset(families, request)
            if result_page is None or len(result_page) == 0:
                return Response({
                    'error': 'No fund families found.',
                    'success': False,
                    'status_code': status.HTTP_404_NOT_FOUND
                }, status=status.HTTP_404_NOT_FOUND)

            # Serialize the paginated result
            serializer = FundFamilySerializer(result_page, many=True)

            # Return paginated response with custom data
            response_data = paginator.get_paginated_response(serializer.data).data
            response_data['success'] = True

            return Response(response_data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist as e:
            logger.warning(f"Object not found: {e}")
            return Response({
                'error': 'FundFamily object not found.',
                'success': False,
                'status_code': status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)

        except ValueError as e:
            logger.error(f"Value Error: {e}")
            return Response({
                'error': 'Invalid value provided.',
                'success': False,
                'status_code': status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.exception(f"Unexpected error occurred: {e}")
            return Response({
                'error': 'Internal server error. Please try again later.',
                'success': False,
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class FetchFundsByFamilyView(APIView):

    permission_classes = [IsAuthenticated]  # Only authenticated users can access this view
    def get(self, request):
        """
        Handle GET request to fetch mutual fund data from a third-party API, 
        save it to the database, and return the results.

        The function performs the following tasks:
        1. Fetches mutual fund data from a third-party API using the `fetch_funds_from_api` method.
        2. Attempts to save the fetched funds into the local database using the `save_funds_to_db` method.
        3. Returns a detailed response with the results of the operation:
            - `created_funds`: List of mutual funds successfully saved to the database.
            - `failed_funds`: List of mutual funds that failed to save, along with their validation errors.
            - `message`: A message indicating the success of the operation.
            - `success`: Boolean indicating whether the operation was successful or not.

        Expected Responses:
            - 201 Created: If mutual funds are fetched and saved successfully.
            - 400 Bad Request: If there are validation or input issues (e.g., failed API request or invalid data).
            - 500 Internal Server Error: For any unexpected errors during the process.
        """

        try:
            # Fetch mutual fund data from the API
            data = self.fetch_funds_from_api()

            # Save the fetched funds into the database
            created_funds, failed_funds = self.save_funds_to_db(data)

            # Return a success response with details about created and failed funds
            return Response({
                "message": "Funds fetched and saved successfully!",
                "created_funds": created_funds,  # List of successfully created funds
                "failed_funds": failed_funds,    # List of failed funds with validation errors
                "success": True,  # Indicate successful execution
            }, status=status.HTTP_201_CREATED)  # HTTP 201 indicates successful creation

        except (ValueError, DRFValidationError) as error:
            # Handle specific errors like failed API request or serializer validation errors
            logger.error(f"Error: {error}")
            return Response({
                'error': str(error),
                'success': False
            }, status=status.HTTP_400_BAD_REQUEST)  # HTTP 400 for bad requests

        except Exception as error:
            # Catch any other unforeseen errors and log them
            logger.exception(f"Exception is: {error}")
            return Response({
                'error': f"{error}",
                'success': False
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  # HTTP 500 for server errors



    def fetch_funds_from_api(self):
        """
        Function to call a third-party API and fetch mutual fund data.
        Handles API request and response validation.
        """
        try:
            # Send GET request to the third-party API using provided headers and parameters
            response = requests.get(
                os.getenv('RAPID_API_URL'),
                headers={ 
                    "x-rapidapi-key": os.getenv('RAPIDAPI_KEY'),
                    "x-rapidapi-host": os.getenv('RAPIDAPI_HOST')
                },
                params={"Scheme_Type": "Open"}  # Fetching only open-ended mutual funds
            )

            # Check if the API response status is successful (HTTP 200)
            if response.status_code != 200:
                raise ValueError("Failed to fetch schemes from third-party API")

            # Return the response as JSON if successful
            return response.json()

        except requests.exceptions.RequestException as e:
            # Catch any exceptions during the API request (network issues, etc.)
            logger.error(f"Error in API request: {e}")
            raise ValueError("API Request failed")  # Raise a value error to handle it in the main function

    def save_funds_to_db(self, data):
        """
        Function to save fetched mutual fund data into the database.
        It attempts to create records in the MutualFund table.
        Returns a list of created funds and failed fund data.
        """
        created_funds = []  # List to store names of successfully created funds
        failed_funds = []  # List to store funds that failed to be created (along with errors)

        # Iterate over each fund item fetched from the API response
        for item in data:
            if item['Scheme_Type'] == 'Open Ended Schemes':
                # Prepare data to be serialized into the MutualFund model
                serializer = MutualFundSerializer(data={
                    "scheme_code": item["Scheme_Code"],  # Unique identifier for each scheme
                    "isin_growth": item.get("ISIN_Div_Payout_ISIN_Growth"),  # ISIN for Growth option
                    "isin_reinvestment": item.get("ISIN_Div_Reinvestment"),  # ISIN for Dividend Reinvestment
                    "scheme_name": item["Scheme_Name"],  # Name of the scheme
                    "nav": float(item["Net_Asset_Value"]),  # NAV (Net Asset Value) of the scheme
                    "nav_date": parse_date(item["Date"]),  # Parse the date for NAV
                    "scheme_type": item["Scheme_Type"],  # Type of scheme (Open/Closed)
                    "scheme_category": item["Scheme_Category"],  # Category of scheme (Equity/Debt)
                    "fund_family_name": item["Mutual_Fund_Family"],  # Name of the fund family
                })

                # Validate the serializer data and save it to the database if valid
                if serializer.is_valid():
                    serializer.save()  # Save the mutual fund data to the database
                    created_funds.append(item.get('Scheme_Name'))  # Add the name to created funds list
                else:
                    # If validation fails, store the errors along with the scheme name
                    failed_funds.append({
                        "scheme_name": item.get('Scheme_Name'),
                        "errors": serializer.errors  # List the validation errors
                    })

        # Return both created and failed fund lists
        return created_funds, failed_funds



class BuyFundView(APIView):
    """
    API view to allow authenticated users to purchase a mutual fund.

    The view validates the user's input (scheme_code, units, and invested_amount), 
    checks the availability of the mutual fund using the scheme_code, and creates a 
    portfolio entry for the authenticated user upon successful validation. The user 
    is required to provide a valid scheme_code, the number of units they wish to purchase, 
    and the amount they want to invest. 

    The process involves:
    1. Validating the provided inputs (units and invested_amount should be numbers > 0).
    2. Checking if the mutual fund with the provided scheme_code exists.
    3. Creating a new portfolio entry for the user with the mutual fund details.
    4. Returning a response with the created portfolio or error details.

    Expected Responses:
        - 201 Created: On successful creation of the portfolio entry.
        - 400 Bad Request: For invalid input data or failed validation.
        - 404 Not Found: If the specified mutual fund does not exist.
        - 500 Internal Server Error: For unexpected server issues.
    """

    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can access this endpoint

    def post(self, request):
        """
        Handle POST request to purchase mutual fund. 
        Validates input data, checks for the existence of the mutual fund, 
        and creates a portfolio entry for the user.
        """
        try:
            # Retrieve the scheme_code, units, and invested_amount from the request data
            scheme_code = request.data.get('scheme_code')
            units = request.data.get('units')
            invested_amount = request.data.get('invested_amount')

            # Input validation: Ensure all fields are provided
            if not scheme_code or not units or not invested_amount:
                return Response({
                    "error": "Invalid purchase details. All fields are required."
                }, status=status.HTTP_400_BAD_REQUEST)  # Return 400 if any field is missing

            try:
                # Try converting units and invested_amount to floats
                units = float(units)
                invested_amount = float(invested_amount)
            except ValueError:
                # If conversion fails, raise an error
                raise ValueError("Units and Invested Amount must be numbers.")

            # Ensure both units and invested_amount are greater than zero
            if units <= 0 or invested_amount <= 0:
                raise ValueError("Units and Invested Amount must be greater than zero.")
            
            try:
                # Retrieve the MutualFund object based on the scheme_code
                mutual_fund = MutualFund.objects.get(scheme_code=scheme_code)
            except MutualFund.DoesNotExist:
                # If the mutual fund does not exist, return an error response
                return Response({
                    "error": "Mutual Fund not found.",
                    "success": False
                }, status=status.HTTP_404_NOT_FOUND)  # Return 404 if the mutual fund is not found

            # Create a new portfolio entry for the user
            portfolio = Portfolio.objects.create(
                user=request.user,  # The portfolio is tied to the authenticated user
                mutual_fund=mutual_fund,  # The mutual fund the user is purchasing
                units=units,  # Number of units being purchased
                invested_amount=invested_amount  # Amount invested
            )

            # Serialize the newly created portfolio object for the response
            serializer = PortfolioSerializer(portfolio)

            # Return a successful response with the created portfolio data
            return Response({
                'data': serializer.data,
                'success': True
            }, status=status.HTTP_201_CREATED)  # HTTP 201 indicates resource creation

        except (ValueError, DRFValidationError) as error:
            # Handle validation errors and log them
            logger.error(f"Validation Error: {error}")
            return Response({
                'error': str(error),
                'success': False
            }, status=status.HTTP_400_BAD_REQUEST)  # Return 400 if there's a validation error

        except Exception as error:
            # Catch any other unforeseen errors, log them, and return a 500 response
            logger.exception(f"Unexpected Error: {error}")
            return Response({
                'error': f"Unexpected error occurred: {error}",
                'success': False
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  # HTTP 500 for server errors



class PortfolioView(APIView):
    """
    API view to retrieve and view the user's portfolio.
    This view returns the list of mutual funds a user has invested in.
    Only accessible by authenticated users.
    """
    
    permission_classes = [IsAuthenticated] 
    def get(self, request):
        """
        Handle GET request to retrieve the authenticated user's portfolio.
        Fetches all portfolio entries for the currently authenticated user.

        Parameters:
            - `request`: The HTTP request object that contains the authenticated user info.

        Response:
            - A JSON object with:
                - `data`: A list of the portfolio items (mutual funds the user has invested in).
                - `success`: Boolean indicating success (`True` or `False`).
            - Status Code:
                - `200 OK` if the data is successfully retrieved.
                - `500 Internal Server Error` if an unexpected error occurs.
        """
        try:
            # Fetch the portfolio for the authenticated user
            portfolio = Portfolio.objects.filter(user=request.user)
            
            # Serialize the portfolio data
            serializer = PortfolioSerializer(portfolio, many=True)
            
            # Return a successful response with the serialized portfolio data
            return Response({
                'data': serializer.data,
                'success': True
            }, status=status.HTTP_200_OK) 

        except Exception as error:
            # Log any unexpected errors that occur
            logger.exception(f"Exception is :  {error}")
            
            # Return an error response with a 500 status code in case of any issues
            return Response({
                'error': f"{error}",
                'success': False
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
