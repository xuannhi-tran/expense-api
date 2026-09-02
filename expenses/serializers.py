from rest_framework import serializers
from .models import Expense

class ExpenseSerializer(serializers.ModelSerializer):
    category = serializers.CharField(required=True)

    class Meta:
        model = Expense
        fields = ['id', 'name', 'amount', 'category', 'created_at', 'updated_at']
        read_only_fielts = ['created_at', 'updated_at',]

    def validate_name(self, value):
        if (value == ""):
            raise serializers.ValidationError("Expense name cannot be empty.")
        return value

    def validate_amount(self, value):
        if (value <= 0):
            raise serializers.ValidationError("Amount must be greater than 0.")
        return value
    
    def validate_category(self, value):
        if (value == ''):
            raise serializers.ValidationError("Category cannot be empty.")
        return value