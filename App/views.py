from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import ProductSerializer, UserSerializer, CartSerializer, ReviewSerializer
from .models import Product, Cart, Category, Review
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

@csrf_exempt
def ListCreateCartItem(request):
    if request.method == "GET":
        return ListCartItems(request)
    elif request.method == "POST":
        return AddCartItem(request)

@csrf_exempt
def UpdateDeleteCartItem(request, product_id):
    if request.method == "PATCH":
        return UpdateCartItemQuantity(request, product_id)
    elif request.method == "DELETE":
        return DeleteCartItem(request, product_id)

@csrf_exempt
def ListCreateProduct(request):
    if request.method == "GET":
        return ListProducts(request)
    elif request.method == "POST":
        return CreateProduct(request)

@csrf_exempt
def ListUpdateDeleteProduct(request, id):
    if request.method == "GET":
        return ListSingleProduct(request, id)
    elif request.method == "PATCH":
        return UpdateProduct(request, id)
    elif request.method == "DELETE":
        return DeleteProduct(request, id)


### CART SECTION ###
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ListCartItems(request):
    user = get_object_or_404(User, username=request.user.username)
    items = Cart.objects.filter(user=user)
    serialized_items = CartSerializer(items, many=True)
    return Response(serialized_items.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AddCartItem(request):
    product_id = request.POST.get('product_id')
    quantity = request.POST.get('quantity')

    if product_id and quantity:
        user = get_object_or_404(User, username=request.user.username)
        product = get_object_or_404(Product, id=product_id)
        
        try:
            Cart.objects.create(user=user, product=product, quantity=quantity)
            return Response({'message': 'cart item added'}, status=status.HTTP_201_CREATED)
        except Exception:
            return Response({'message': 'something went wrong'})
    return Response({'message': 'product_id and quantity required'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteCartItem(request, product_id):
    try:
        user = get_object_or_404(User, username=request.user.username)
        item = Cart.objects.filter(user=user).get(product=product_id)
        deleted_item = Cart.delete(item)

        if deleted_item: 
            return Response({'message': 'item deleted from cart'})
    except Cart.DoesNotExist:
        return Response({'message': 'product not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'message': str(e)})


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def UpdateCartItemQuantity(request, product_id):
    try:
        user = get_object_or_404(User, username=request.user.username)
        cart_item = Cart.objects.filter(user=user).get(product=product_id)
        serialized_cart = CartSerializer(cart_item, data=request.data)

        if serialized_cart.is_valid():
            serialized_cart.save()
            return Response(serialized_cart.data)
        return Response(serialized_cart.errors)
    except Cart.DoesNotExist:
        return Response({'message': 'product not found'}, status=status.HTTP_404_NOT_FOUND)


### PRODUCT SECTION ###
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ListProducts(request):
    queryset = Product.objects.all()
    products = ProductSerializer(queryset, many=True)
    return Response(products.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ListSingleProduct(request, id):
    try:
        queryset = Product.objects.select_related('category').get(id=id)
        serialized = ProductSerializer(queryset)
        return Response(serialized.data)
    except Product.DoesNotExist:
        return Response({'message': 'product not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def CreateProduct(request):
    product = ProductSerializer(data=request.data)
    validity = product.is_valid()
    if validity:
        product.save()
        return Response({'message': 'success'})
    return Response({'valid': validity, 'retrieved_data': product.data, 'validated_data': product.validated_data, 'errors': product.errors})


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
    except Exception as e:
        return Response({'message': str(e)})


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


### USER SECTION ###
class ListUsers(generics.ListAPIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def DeleteUser(request):
    username = request.POST.get('username')
    user = get_object_or_404(User, username=username)
    User.delete(user)
    return Response({'message': f'user <{user.username}> deleted'})


### CATEGORY SECTION ###
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def BulkAddCategory(request):
    categories = list()

    for elem in request.data:
        categories.append(Category(id=elem['id'], name=elem['name'], count=elem['count']))
    
    try:
        Category.objects.bulk_create(categories)
        return Response({'success': 'categories created'})
    except Exception:
        return Response({'message': 'some exception occured'})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def DeleteCategory(request, id):
    category = get_object_or_404(Category, id=id)
    Category.delete(category)
    return Response({'message': f'category<id:{id}> deleted'})


### REVIEW SECTION ###
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ListReviews(request):
    queryset = Review.objects.all()
    reviews = ReviewSerializer(queryset, many=True)
    return Response(reviews.data)
