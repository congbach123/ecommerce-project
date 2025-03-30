import requests
from django.conf import settings
from requests.exceptions import RequestException

BASE_URL = "http://localhost:8000/api"

class ServiceCommunicator:
    @staticmethod
    def call_service(service, endpoint, method='GET', data=None, headers=None):
        """
        Make a call to another microservice
        """
        url = f"{BASE_URL}/{service}/{endpoint}"
        default_headers = {'Content-Type': 'application/json'}
        
        if headers:
            default_headers.update(headers)
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=default_headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=default_headers)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=default_headers)
            elif method == 'DELETE':
                response = requests.delete(url, headers=default_headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            # In a real application, you would log this error
            print(f"Service communication error: {e}")
            return None