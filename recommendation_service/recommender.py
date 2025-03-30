import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
import requests

class RecommendationEngine:
    def __init__(self):
        self.user_interactions = None
        self.product_data = None
        self.user_item_matrix = None
        self.similarity_matrix = None
    
    def load_data(self):
        # Load user interactions
        response = requests.get('http://localhost:8000/api/recommendations/interactions/')
        interactions_data = response.json()
        self.user_interactions = pd.DataFrame(interactions_data)
        
        # Load product data
        response = requests.get('http://localhost:8000/api/products/products/')
        product_data = response.json()
        self.product_data = pd.DataFrame(product_data)
    
    def create_user_item_matrix(self):
        # Create a weighted score for each interaction
        self.user_interactions['score'] = (
            self.user_interactions['viewed'] * 1 +
            self.user_interactions['added_to_cart'] * 3 +
            self.user_interactions['purchased'] * 5 +
            self.user_interactions['rating'].fillna(0)
        )
        
        # Create user-item matrix
        self.user_item_matrix = self.user_interactions.pivot_table(
            index='user_id', 
            columns='product_id', 
            values='score', 
            fill_value=0
        )
    
    def calculate_similarity(self):
        # Calculate item-item similarity matrix
        self.similarity_matrix = cosine_similarity(self.user_item_matrix.T)
        
        # Create a DataFrame for the similarity matrix
        self.similarity_df = pd.DataFrame(
            self.similarity_matrix,
            index=self.user_item_matrix.columns,
            columns=self.user_item_matrix.columns
        )
    
    def get_recommendations(self, user_id, n=5):
        if user_id not in self.user_item_matrix.index:
            # For new users, return popular items
            return self.get_popular_items(n)
        
        # Get items the user has interacted with
        user_items = self.user_interactions[self.user_interactions['user_id'] == user_id]['product_id'].unique()
        
        # Calculate recommendation scores
        scores = defaultdict(float)
        for item in user_items:
            if item not in self.similarity_df.index:
                continue
            
            # Get similarity scores for this item
            similar_items = self.similarity_df[item]
            
            # Add weighted scores for all similar items
            for similar_item, similarity in similar_items.items():
                if similar_item not in user_items:
                    scores[similar_item] += similarity
        
        # Sort items by score and return top n
        top_items = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:n]
        return [item_id for item_id, score in top_items]
    
    def get_popular_items(self, n=5):
        # For new users, return the most popular items
        item_counts = self.user_interactions.groupby('product_id').size().sort_values(ascending=False)
        return item_counts.index[:n].tolist()