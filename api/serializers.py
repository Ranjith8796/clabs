from rest_framework import serializers
from .models import account, destination

class accountserializer(serializers.ModelSerializer):
    class Meta:
        model = account
        fields = ['email_id', 'account_id', 'account_name', 'token', 'website' ]

class destinationserializer(serializers.ModelSerializer):
    class Meta:
        model = destination
        fields = ['id', 'account_id', 'distination_url', 'http_method', 'headers' ]
