from django.db import models
from accounts.models import User

# Represents a Fund Family (like HDFC Mutual Fund, ICICI Mutual Fund etc.)
class FundFamily(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Name of the fund family; must be unique
    created_at = models.DateTimeField(auto_now_add=True)  # Auto timestamp when the record is created
    updated_at = models.DateTimeField(auto_now=True)      # Auto timestamp when the record is updated

    def __str__(self):  
        # return f"id: {self.id} -- Name: {self.name}"
        return f"{self.name}"

# Represents an individual Mutual Fund Scheme
class MutualFund(models.Model):
    scheme_code = models.IntegerField(unique=True)               # Unique code for each mutual fund (real-world: AMFI code)
    isin_growth = models.CharField(max_length=50, blank=True, null=True)       # ISIN code for Growth option (optional)
    isin_reinvestment = models.CharField(max_length=50, blank=True, null=True) # ISIN code for Dividend Reinvestment option (optional)
    scheme_name = models.CharField(max_length=255)                # Official name of the mutual fund scheme
    nav = models.FloatField()                                     # Latest Net Asset Value
    nav_date = models.DateField()                                 # NAV Date
    scheme_type = models.CharField(max_length=100)                # Type: e.g., "Open Ended", "Close Ended"
    scheme_category = models.CharField(max_length=100)            # Category: e.g., "Equity", "Debt", "Hybrid"
    fund_family = models.ForeignKey(FundFamily, on_delete=models.CASCADE)  # Link to the parent fund family
    created_at = models.DateTimeField(auto_now_add=True)          # Timestamp of creation
    updated_at = models.DateTimeField(auto_now=True)              # Timestamp of last update

    def __str__(self):
        return f"id: {self.id}---> SchemeName: {self.scheme_name}"

# Represents a User's Investment in a particular Mutual Fund (Portfolio Holding)
class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fund_portfolios')  # User who owns this portfolio
    mutual_fund = models.ForeignKey(MutualFund, on_delete=models.CASCADE)                     # Mutual fund invested in
    units = models.FloatField()                                                                 # Number of units purchased
    invested_amount = models.FloatField()                                                       # Total money invested
    purchase_date = models.DateTimeField(auto_now_add=True)  # When the purchase was made
    created_at = models.DateTimeField(auto_now_add=True)     # Timestamp of creation
    updated_at = models.DateTimeField(auto_now=True)         # Timestamp of last update

    def __str__(self):
        return f"{self.id} ---- {self.user.username} - {self.mutual_fund.scheme_name}"
