import requests
import json
import random
from datetime import datetime

BASE_URL = "http://localhost:8000/api"
token = None

def print_step(step):
    print("\n" + "=" * 80)
    print(f"STEP: {step}")
    print("=" * 80)

def register_user():
    print_step("Registering a new user")
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    data = {
        "username": f"testuser_{timestamp}",
        "email": f"test_{timestamp}@example.com",
        "password": "testpassword123",
        "password2": "testpassword123",
        "first_name": "Test",
        "last_name": "User",
        "phone_number": "1234567890",
        "address": "123 Test Street, Test City"
    }
    
    response = requests.post(f"{BASE_URL}/users/register/", json=data)
    
    if response.status_code == 201:
        print("User registered successfully!")
        return data["username"], data["password"]
    else:
        print(f"Failed to register user: {response.status_code}")
        print(response.text)
        return None, None

def login_user(username, password):
    print_step("Logging in")
    
    data = {
        "username": username,
        "password": password
    }
    
    response = requests.post(f"{BASE_URL}/users/login/", json=data)
    
    if response.status_code == 200:
        global token
        token = response.json().get("token")
        print(f"Login successful! Token: {token}")
        return True
    else:
        print(f"Failed to login: {response.status_code}")
        print(response.text)
        return False

def get_categories():
    print_step("Getting product categories")
    
    response = requests.get(f"{BASE_URL}/products/categories/")
    
    if response.status_code == 200:
        categories = response.json()
        print(f"Found {len(categories)} categories:")
        for cat in categories:
            print(f"  - {cat['name']}: {cat['description']}")
        return categories
    else:
        print(f"Failed to get categories: {response.status_code}")
        print(response.text)
        return []

def get_products():
    print_step("Getting products")
    
    response = requests.get(f"{BASE_URL}/products/products/")
    
    if response.status_code == 200:
        products = response.json()
        print(f"Found {len(products)} products:")
        for i, product in enumerate(products[:5]):  # Show only first 5
            print(f"  - {product['name']}: ${product['price']}")
        
        if len(products) > 5:
            print(f"  ... and {len(products) - 5} more")
            
        return products
    else:
        print(f"Failed to get products: {response.status_code}")
        print(response.text)
        return []

def add_to_cart(product_id):
    print_step(f"Adding product {product_id} to cart")
    
    headers = {"Authorization": f"Token {token}"}
    data = {
        "product_id": product_id,
        "quantity": 1
    }
    
    response = requests.post(f"{BASE_URL}/cart/add_item/", json=data, headers=headers)
    
    if response.status_code == 200:
        item = response.json()
        print(f"Added to cart: {item['product_name']} (Quantity: {item['quantity']})")
        return True
    else:
        print(f"Failed to add to cart: {response.status_code}")
        print(response.text)
        return False

def view_cart():
    print_step("Viewing cart")
    
    headers = {"Authorization": f"Token {token}"}
    
    response = requests.get(f"{BASE_URL}/cart/", headers=headers)
    
    if response.status_code == 200:
        cart = response.json()
        items = cart.get("items", [])
        total = cart.get("total", 0)
        
        print(f"Cart has {len(items)} items with total value: ${total}")
        for item in items:
            print(f"  - {item['product_name']}: ${item['price']} x {item['quantity']} = ${item['total']}")
            
        return cart
    else:
        print(f"Failed to view cart: {response.status_code}")
        print(response.text)
        return None

def checkout():
    print_step("Checking out")
    
    headers = {"Authorization": f"Token {token}"}
    data = {
        "shipping_address": "123 Test Street, Test City"
    }
    
    response = requests.post(f"{BASE_URL}/orders/create_from_cart/", json=data, headers=headers)
    
    if response.status_code == 201:
        order = response.json()
        print(f"Order #{order['id']} created successfully with total: ${order['total_amount']}")
        
        print("Order items:")
        for item in order.get("items", []):
            print(f"  - {item['product_name']}: ${item['price']} x {item['quantity']}")
            
        return order
    else:
        print(f"Failed to checkout: {response.status_code}")
        print(response.text)
        return None

def view_orders():
    print_step("Viewing orders")
    
    headers = {"Authorization": f"Token {token}"}
    
    response = requests.get(f"{BASE_URL}/orders/", headers=headers)
    
    if response.status_code == 200:
        orders = response.json()
        print(f"Found {len(orders)} orders:")
        
        for order in orders:
            print(f"Order #{order['id']}: ${order['total_amount']} - Status: {order['status']}")
            print(f"  Items: {len(order.get('items', []))}")
            
        return orders
    else:
        print(f"Failed to view orders: {response.status_code}")
        print(response.text)
        return []

def get_recommendations():
    print_step("Getting product recommendations")
    
    headers = {"Authorization": f"Token {token}"}
    
    response = requests.get(f"{BASE_URL}/recommendations/interactions/get_recommendations/", headers=headers)
    
    if response.status_code == 200:
        recommendations = response.json()
        print(f"Got {len(recommendations)} recommendations:")
        
        for product in recommendations:
            print(f"  - {product['name']}: ${product['price']}")
            
        return recommendations
    else:
        print(f"Failed to get recommendations: {response.status_code}")
        print(response.text)
        return []

def main():
    # Register and login
    username, password = register_user()
    if not username:
        return
    
    if not login_user(username, password):
        return
    
    # Browse products
    categories = get_categories()
    products = get_products()
    
    if not products:
        return
    
    # Add some products to cart
    for _ in range(2):
        product = random.choice(products)
        add_to_cart(product['id'])
    
    # View cart
    cart = view_cart()
    
    if not cart:
        return
    
    # Checkout
    order = checkout()
    
    if not order:
        return
    
    # View orders
    orders = view_orders()
    
    # Get recommendations
    recommendations = get_recommendations()
    
    print("\nTest completed successfully!")

if __name__ == "__main__":
    main()