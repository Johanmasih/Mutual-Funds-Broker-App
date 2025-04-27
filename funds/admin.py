from django.contrib import admin
from funds.models import Portfolio, FundFamily, MutualFund
# Register your models here.
admin.site.register(Portfolio)
admin.site.register(MutualFund)
admin.site.register(FundFamily)