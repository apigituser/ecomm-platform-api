from django.http import JsonResponse
from rest_framework import generics
from rest_framework.views import APIView, csrf_exempt
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import ProductSerializer, UserSerializer
from .models import Product
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def CreateProduct(request):
    product = ProductSerializer(data=request.data)
    validity = product.is_valid()
    if validity:
        product.save()
        return Response({'message': 'success'})
    return Response({'valid': validity, 'retrieved_data': product.data, 'validated_data': product.validated_data, 'errors': product.errors})

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
