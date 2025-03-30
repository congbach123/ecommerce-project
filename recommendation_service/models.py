from django.db import models
from django.conf import settings

class UserInteraction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product_id = models.PositiveIntegerField()
    viewed = models.BooleanField(default=False)
    added_to_cart = models.BooleanField(default=False)
    purchased = models.BooleanField(default=False)
    rating = models.PositiveSmallIntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'product_id')
    
    def __str__(self):
        return f"{self.user.username} - Product {self.product_id}"