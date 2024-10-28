import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class DistanceCalculatorView(APIView):

    def get_coordinates(self, city_name):
        """Get coordinates from OpenCage API for a given city name."""
        opencage_url = "https://api.opencagedata.com/geocode/v1/json"
        params = {
            'q': city_name,
            'key': settings.OPENCAGE_API_KEY,
        }
        response = requests.get(opencage_url, params=params)
        data = response.json()
        
        if data['results']:
            geometry = data['results'][0]['geometry']
            return geometry['lat'], geometry['lng']
        else:
            return None, None

    def get_distance(self, source_coords, dest_coords):
        """Calculate distance using OpenRouteService API based on coordinates."""
        openrouteservice_url = "https://api.openrouteservice.org/v2/directions/driving-car"
        headers = {
            'Authorization': settings.OPENROUTESERVICE_API_KEY,
            'Content-Type': 'application/json'
        }
        coords = {
            "coordinates": [source_coords[::-1], dest_coords[::-1]]  # reverse for longitude, latitude format
        }
        response = requests.post(openrouteservice_url, headers=headers, json=coords)
        data = response.json()
        
        if 'routes' in data and data['routes']:
            distance_meters = data['routes'][0]['summary']['distance']
            distance_km = distance_meters / 1000  # Convert to kilometers
            return distance_km
        else:
            return None

    def post(self, request):
        source_city = request.data.get('source_city')
        destination_city = request.data.get('destination_city')

        if not source_city or not destination_city:
            return Response({"error": "Please provide both source and destination cities."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Get coordinates for source and destination cities
        source_coords = self.get_coordinates(source_city)
        dest_coords = self.get_coordinates(destination_city)

        if None in source_coords or None in dest_coords:
            return Response({"error": "Could not find coordinates for one or both cities."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Get distance based on coordinates
        distance = self.get_distance(source_coords, dest_coords)

        if distance is None:
            return Response({"error": "Could not calculate distance."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        distance_miles = round(distance * 0.621371)

        return Response({
            "source_city": source_city,
            "destination_city": destination_city,
            "distance_miles": distance_miles
        }, status=status.HTTP_200_OK)
