from rest_framework import serializers
from .models import FundFamily, MutualFund, Portfolio
from rest_framework import serializers
from .models import FundFamily, MutualFund


class FundFamilySerializer(serializers.ModelSerializer):
    """Serializer for FundFamily model, including 'id' and 'name'."""
    class Meta:
        model = FundFamily
        fields = ['id', 'name']

class MutualFundSerializer(serializers.ModelSerializer):
    """Serializer for MutualFund model, including fields and custom fund_family_name for input."""
    fund_family_name = serializers.CharField(write_only=True)
    
    class Meta:
        model = MutualFund
        fields = [
            'scheme_code', 'isin_growth', 'isin_reinvestment', 'scheme_name', 
            'nav', 'nav_date', 'scheme_type', 'scheme_category', 'fund_family', 'fund_family_name'
        ]
        extra_kwargs = {'fund_family': {'read_only': True}}

    def create(self, validated_data):
        """Create or get FundFamily and associate it with the mutual fund."""
        fund_family_name = validated_data.pop('fund_family_name')
        fund_family, created = FundFamily.objects.get_or_create(name=fund_family_name)
        validated_data['fund_family'] = fund_family
        return super().create(validated_data)

class PortfolioSerializer(serializers.ModelSerializer):
    """Serializer for Portfolio model with calculated current_value field."""
    scheme_name = serializers.CharField(source="mutual_fund.scheme_name", read_only=True)
    nav = serializers.FloatField(source="mutual_fund.nav", read_only=True)
    current_value = serializers.SerializerMethodField()

    class Meta:
        model = Portfolio
        fields = ['scheme_name', 'units', 'invested_amount', 'current_value', 'nav']

    def get_current_value(self, obj):
        """Calculate current value based on units and NAV."""
        return round(obj.units * obj.mutual_fund.nav, 2)
