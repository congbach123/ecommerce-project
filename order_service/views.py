from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
import requests
from .models import Order, OrderItem
from .serializers import OrderSerializer
from django.db import transaction

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    @transaction.atomic
    @action(detail=False, methods=['post'])
    def create_from_cart(self, request):
        # Get user's cart
        response = requests.get(
            'http://localhost:8000/api/cart/',
            headers={'Authorization': request.headers.get('Authorization')}
        )
        
        if response.status_code != 200:
            return Response({'error': 'Could not retrieve cart'}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        cart_data = response.json()
        
        if not cart_data.get('items'):
            return Response({'error': 'Cart is empty'}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            shipping_address=request.data.get('shipping_address', request.user.address),
            total_amount=sum(item['price'] * item['quantity'] for item in cart_data['items'])
        )
        
        # Create order items
        for item in cart_data['items']:
            OrderItem.objects.create(
                order=order,
                product_id=item['product_id'],
                product_name=item['product_name'],
                price=item['price'],
                quantity=item['quantity']
            )
        
        # Clear the cart
        requests.post(
            'http://localhost:8000/api/cart/clear/',
            headers={'Authorization': request.headers.get('Authorization')}
        )
        
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)