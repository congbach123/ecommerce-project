from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import UserInteraction
from .serializers import UserInteractionSerializer
from .recommender import RecommendationEngine

class UserInteractionViewSet(viewsets.ModelViewSet):
    serializer_class = UserInteractionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserInteraction.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def record_interaction(self, request):
        product_id = request.data.get('product_id')
        interaction_type = request.data.get('interaction_type')
        rating = request.data.get('rating')
        
        interaction, created = UserInteraction.objects.get_or_create(
            user=request.user,
            product_id=product_id,
            defaults={
                'viewed': False,
                'added_to_cart': False,
                'purchased': False,
                'rating': None
            }
        )
        
        if interaction_type == 'view':
            interaction.viewed = True
        elif interaction_type == 'cart':
            interaction.added_to_cart = True
        elif interaction_type == 'purchase':
            interaction.purchased = True
        
        if rating is not None:
            interaction.rating = rating
        
        interaction.save()
        
        return Response(UserInteractionSerializer(interaction).data)
    
    @action(detail=False, methods=['get'])
    def get_recommendations(self, request):
        engine = RecommendationEngine()
        engine.load_data()
        engine.create_user_item_matrix()
        engine.calculate_similarity()
        
        recommendations = engine.get_recommendations(request.user.id)
        
        # Get product details
        import requests
        product_data = []
        for product_id in recommendations:
            response = requests.get(f'http://localhost:8000/api/products/products/{product_id}/')
            if response.status_code == 200:
                product_data.append(response.json())
        
        return Response(product_data)