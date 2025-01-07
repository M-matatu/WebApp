from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render,get_object_or_404,Http404,redirect
from .models import Fare
from geopy.distance import geodesic
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from django.utils import timezone
from .models import Bus
from .serializers import BusSerializer
from django.http import JsonResponse
from django.views import View
from .models import UserBalance
from django.contrib.auth.models import User

from django_daraja.mpesa.core import MpesaClient

@permission_classes([AllowAny])
@csrf_exempt
class BalanceView(View):
    def get(self, request):
        username = request.GET.get('username')
        
        if not username:
            return JsonResponse({'error': 'Username parameter is required'}, status=400)

        try:
            user = User.objects.get(username=username)
            user_balance = UserBalance.objects.get(user=user)
            return JsonResponse({'balance': str(user_balance.balance)}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except UserBalance.DoesNotExist:
            return JsonResponse({'error': 'Balance not found for this user'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        

@permission_classes([AllowAny])
@csrf_exempt
def pay(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            phone_number = data.get('phone_number')
            amount = data.get('amount', 1)
            username = data.get('username')

            cl = MpesaClient()
            response = cl.stk_push(phone_number, amount, 'reference', 'Description', 'https://customerdasshboard.onrender.com/dashboard')

            if response.get('ResponseCode') == '0':
                user = User.objects.get(username=username)
                user_balance = UserBalance.objects.get(user=user)
                user_balance.balance += decimal.Decimal(amount)
                user_balance.save()

                return JsonResponse({'success': 'Payment successful', 'new_balance': str(user_balance.balance)}, status=200)

            return JsonResponse({'error': 'Payment failed', 'details': response}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except UserBalance.DoesNotExist:
            return JsonResponse({'error': 'Balance not found for this user'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@permission_classes([AllowAny])
@csrf_exempt
def edit_bus(request, id):
    if request.method == 'PUT':
        try:
            bus = get_object_or_404(Bus, id=id)
            data = json.loads(request.body)

            bus.routeStart = data.get('routeStart', bus.routeStart)
            bus.routeEnd = data.get('routeEnd', bus.routeEnd)
            bus.status = data.get('status', bus.status)
            bus.capacity = data.get('capacity', bus.capacity)
            bus.passengerCount = data.get('passengerCount', bus.passengerCount)
            bus.save()

            return JsonResponse({"message": "Bus updated successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@permission_classes([AllowAny])
@csrf_exempt
def delete_bus(request, id):
    if request.method == 'DELETE':
        try:
            bus = get_object_or_404(Bus, id=id)
            bus.delete()

            return JsonResponse({"message": "Bus deleted successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@permission_classes([AllowAny])
class BusListCreateView(APIView):
    # Handle GET requests to display buses
    def get(self, request, *args, **kwargs):
        buses = Bus.objects.all()
        serializer = BusSerializer(buses, many=True)
        return Response(serializer.data)

    # Handle POST requests to add a new bus
    def post(self, request, *args, **kwargs):
        serializer = BusSerializer(data=request.data)
        if serializer.is_valid():
            bus = serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):

    try:
        data = request.data
        username = data['username']
        email = data['email']
        password = data['password']
        if User.objects.filter(username=username).exists():
            return Response({"detail": "User already exists. Log in"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"detail": "User with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
        )
        user.save()
        return Response({"detail": "User created successfully!"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    try:
        if isinstance(request.data, dict) and '_content' not in request.data:
            data = request.data
            print("Parsed as JSON:", data)
        else:
            data = dict(request.data)
            data_json = data.get('_content', '')
            data_json = data_json[0].replace("\r\n", "")  
            data = json.loads(data_json)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token
            return Response({
                'refresh': str(refresh),
                'access': str(access),
                'user': {
                    'email': user.email,
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([AllowAny])
@csrf_exempt
def Faresetting(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            route_id = data.get('route_id')
            route_start = data.get('route_start')
            route_end = data.get('route_end')
            rate = data.get('Rate')

            # Validate required fields
            if not route_start or not route_end or not route_id or not rate:
                return JsonResponse(
                    {'error': 'route_start, route_end, and Rate are required fields.'}, 
                    status=400
                )

            # Check if a fare with the same route_start and route_end already exists
            existing_fare = Fare.objects.filter(route_start=route_start, route_end=route_end).first()
            if existing_fare:
                return JsonResponse(
                    {'error': 'A fare with the same route_start and route_end already exists.'}, 
                    status=400
                )

            # Save the new fare data to the database
            fare = Fare.objects.create(route_start=route_start, route_id=route_id, route_end=route_end, Rate=rate)
            return JsonResponse(
                {
                    'message': 'Fare created successfully!',
                    'fare': {
                        'route_start': fare.route_start,
                        'route_end': fare.route_end,
                        'route_id': fare.route_id,
                        'Rate': fare.Rate,
                    },
                },
                status=201
            )
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    elif request.method == 'GET':
        # Fetch all fares and include route_start and route_end in the response
        fares = Fare.objects.all()
        fare_list = [
            {   
                'route_id': fare.route_id,
                'route_start': fare.route_start,
                'route_end': fare.route_end,
                'Rate': fare.Rate,
                'updated_at': fare.updated_at,
            }
            for fare in fares
        ]
        return JsonResponse({'fares': fare_list}, status=200)

    else:
        return JsonResponse({'error': 'Invalid HTTP method.'}, status=405)
@csrf_exempt
def update_fare_rate(request, route_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            fare = get_object_or_404(Fare, route_id=route_id)
            fare.Rate = data.get('Rate', fare.Rate)
            fare.updated_at = data.get('updated_at', timezone.now())  # Optional, defaults to now
            fare.save()

            
            return JsonResponse({
                'message': 'Fare rate updated successfully!',
                'Route_start': fare.route_end,
                'Route_end': fare.route_start,
                'Rate': fare.Rate,
                'Updated At': fare.updated_at
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except KeyError:
            return JsonResponse({'error': 'Missing required fields: Rate or updated_at'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)