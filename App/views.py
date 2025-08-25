from django.http import JsonResponse
from rest_framework import generics
from rest_framework.views import APIView, csrf_exempt
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.contrib.auth.models import User
from .serializers import ProductSerializer
from .models import Product
from rest_framework.decorators import api_view, permission_classes

@csrf_exempt
def product_list_create(request):
    if request.method == 'GET':
        return ListProducts(request)
    elif request.method == 'POST':
        return CreateProducts(request)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ListProducts(request):
    products = Product.objects.select_related('category')
    serializer = ProductSerializer(products, many=True)
    return JsonResponse({"products": serializer.data})

@api_view(['POST'])
@permission_classes([IsAdminUser, IsAuthenticated])
def CreateProducts(request):
    return 

## Admin Only
class ListUsers(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        response = list(User.objects.values())
        return JsonResponse({"users": response})

class UserRegistration(APIView):

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")

        if username and password and email:
            user = User.objects.create_user(username, email, password)
            if user is not None:
                return JsonResponse({"status": "registeration successful"})
            return JsonResponse({"status": "user not registered"}, status=400)
        return JsonResponse({"status": "username, password and email are required"}, status=400)

