from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework import status
#from .serializers import UserSerializer
import json
from rest_framework.views import APIView
#from Backend.models import smoke,batt,temperature,soilph,soilprecipitation
#from Backend.models import GSCoordinates,Images
from django.views.decorators.csrf import csrf_exempt 


def homepage(request):
    return HttpResponse("Mmatatu Backend Apis!")


@permission_classes([AllowAny])
class driverapi(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Check if request.data is a dictionary (it will be if the content is JSON)
            if isinstance(request.data, dict) and '_content' not in request.data:
                data = request.data
                print("Parsed as JSON:", data)
            else:
                # Convert QueryDict to a dictionary
                data = dict(request.data)
                print("QueryDict Data:", data)
                
                # Extract JSON content from '_content' key
                data_json = data.get('_content', '')  # Assuming '_content' exists in QueryDict
                print(data_json)
                data_json = data_json[0].replace("\r\n", "")  # Clean up new lines if any
                data = json.loads(data_json)  # Convert JSON string to a Python dictionary
                print("Extracted Data:", data)

            # Extract temperature and humidity
            soilph= data.get('soilph')
            print(soilph)

            # Simple validation check
            if soilph is None:
                return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)
            
            soilph_data = soilph(
                soilph=soilph
                
                
            )
            soilph_data.save()
           
            return Response({"message": "Success", "data": data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@permission_classes([AllowAny])
class passapi(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Check if request.data is a dictionary (it will be if the content is JSON)
            if isinstance(request.data, dict) and '_content' not in request.data:
                data = request.data
                print("Parsed as JSON:", data)
            else:
                # Convert QueryDict to a dictionary
                data = dict(request.data)
                print("QueryDict Data:", data)
                
                # Extract JSON content from '_content' key
                data_json = data.get('_content', '')  # Assuming '_content' exists in QueryDict
                print(data_json)
                data_json = data_json[0].replace("\r\n", "")  # Clean up new lines if any
                data = json.loads(data_json)  # Convert JSON string to a Python dictionary
                print("Extracted Data:", data)
            
            #change this to suit the data on esp
            # Extract location data
            location = data.get('location')
            

            # Simple validation check
            if location is None:
                return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)

           
            location_data = location(
                location=location
                
            )
            location_data.save() 
            return Response({"message": "Success", "data": data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@permission_classes([AllowAny])
class soilprecipitation(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Check if request.data is a dictionary (it will be if the content is JSON)
            if isinstance(request.data, dict) and '_content' not in request.data:
                data = request.data
                print("Parsed as JSON:", data)
            else:
                # Convert QueryDict to a dictionary
                data = dict(request.data)
                print("QueryDict Data:", data)
                
                # Extract JSON content from '_content' key
                data_json = data.get('_content', '')  # Assuming '_content' exists in QueryDict
                print(data_json)
                data_json = data_json[0].replace("\r\n", "")  # Clean up new lines if any
                data = json.loads(data_json)  # Convert JSON string to a Python dictionary
                print("Extracted Data:", data)
            
            #change this to suit the data on esp
            # Extract location data
            soilprecipitation = data.get('soilprecipitation')
            

            # Simple validation check
            if soilprecipitation is None:
                return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)

            
            soilprecipitation = soilprecipitation(
                soilprecipitation=soilprecipitation
            )
            soilprecipitation.save() 
            return Response({"message": "Success", "data": data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

@permission_classes([AllowAny])
class groundstationCoordinates(APIView):
    def post(self, request, *args, **kwargs):

        try:
            if isinstance(request.data, dict) and '_content' not in request.data:
                data = request.data
                print("Parsed as JSON:", data)
            else:
                # Convert QueryDict to a dictionary
                data = dict(request.data)
                print("QueryDict Data:", data)
                
                # Extract JSON content from '_content' key
                data_json = data.get('_content', '')  # Assuming '_content' exists in QueryDict
                print(data_json)
                data_json = data_json[0].replace("\r\n", "")  # Clean up new lines if any
                data = json.loads(data_json)  # Convert JSON string to a Python dictionary
                print("Extracted Data:", data)
                
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            entry = GSCoordinates(data)
            entry.coordinatesave()
            
            if latitude is None or longitude is None:
                return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)

            coords = GSCoordinates(
                latitude=latitude,
                longitude=longitude
                
            )
            coords.save()

            return JsonResponse({'status': 'success', 'message': 'Coordinates updated'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    


def get_gs(request):
    coords = GSCoordinates.objects.first()
    if coords:
        return JsonResponse({
            'latitude': coords.latitude,
            'longitude': coords.longitude
        })
    else:
        return JsonResponse({
            'latitude': None,
            'longitude': None
        })