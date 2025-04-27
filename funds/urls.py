from django.urls import path
from .views import FundFamilyListView, FetchFundsByFamilyView, BuyFundView, PortfolioView

app_name = 'funds'

urlpatterns = [
    path('api/v1/list-fund-families', FundFamilyListView.as_view(), name='list_fund_families'), # List all Fund Families
    path('api/v1/fetch-external-funds', FetchFundsByFamilyView.as_view(), name='fetch_external_funds'),  #Fetch funds from third-party API
    path('api/v1/purchase-fund', BuyFundView.as_view(), name='purchase_fund'),  # Buy/invest in a fund
    path('api/v1/user-portfolio', PortfolioView.as_view(), name='user_portfolio'),  # Get user's bought funds
]
