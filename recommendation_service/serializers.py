from rest_framework import serializers
from .models import UserInteraction

class UserInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInteraction
        fields = ['id', 'user', 'product_id', 'viewed', 
                  'added_to_cart', 'purchased', 'rating', 'timestamp']
        read_only_fields = ['user']