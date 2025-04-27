from celery import shared_task
from .views import FetchFundsByFamilyView

@shared_task
def fetch_and_save_funds():
    """
    Celery task to fetch mutual fund data from a third-party API 
    and save it to the database. This task is triggered asynchronously.
    """
    fetch_funds_view = FetchFundsByFamilyView()

    # Call the view's logic to fetch and save mutual fund data to the database
    try:
        data = fetch_funds_view.fetch_funds_from_api()  # Fetch funds data from API
        created_funds, failed_funds = fetch_funds_view.save_funds_to_db(data)  # Save to DB
        return {
            "created_funds": created_funds,  # List of successfully created funds
            "failed_funds": failed_funds,    # List of failed funds with errors
        }
    except Exception as error:
        return {"error": str(error)}  # Return error message in case of failure
