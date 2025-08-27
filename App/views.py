from django.http import JsonResponse
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import ProductSerializer, UserSerializer
from .models import Product
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

# DELETE A PRODUCT
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def DeleteProduct(request, id):
    try:
        product = Product.objects.get(id=id)
        deleted_product = Product.delete(product)
        return Response({'message': 'product(id:{}) deleted'.format(id)})
    except Product.DoesNotExist:
        return Response({'message': 'product not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'message': str(e)})

# UPDATE A PRODUCT
'''
STEPS TO UPDATE THE PRODUCT
Fetch the product with the requested id
Serialize the received the product using the ProductSerializer
    :parameters -> the product object received, date in the request, partial=True (partial data allowed)
Check if the serialized product is valid:
    if valid -> save the product
    else -> return an error response
'''
@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsAdminUser])
def UpdateProduct(request, id):
    try:
        product = Product.objects.get(id=id)
        serialized_product = ProductSerializer(product, data=request.data, partial=True)
        if serialized_product.is_valid():
            updated_product = serialized_product.save()
            return Response(serialized_product.data)
        return Response(serialized_product.errors)
    except Product.DoesNotExist:
        return Response({'message': 'product not found'}, status=status.HTTP_404_NOT_FOUND)

# CREATE A PRODUCT
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def CreateProduct(request):
    product = ProductSerializer(data=request.data)
    validity = product.is_valid()
    if validity:
        product.save()
        return Response({'message': 'success'})
    return Response({'valid': validity, 'retrieved_data': product.data, 'validated_data': product.validated_data, 'errors': product.errors})

# LIST SINGLE PRODUCT
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ListSingleProduct(request, id):
    try:
        queryset = Product.objects.select_related('category').get(id=id)
        serialized = ProductSerializer(queryset)
        return Response(serialized.data)
    except Product.DoesNotExist:
        return Response({'message': 'product not found'}, status=status.HTTP_404_NOT_FOUND)

# LIST ALL PRODUCTS
class ListProducts(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()

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

### ADMIN SECTION ###
class ListUsers(generics.ListAPIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()
