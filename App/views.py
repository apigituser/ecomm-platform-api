from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import ProductSerializer, UserSerializer, CartSerializer, ReviewSerializer, OrderSerializer
from .models import Product, Cart, Category, Review, Order
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
    product = get_object_or_404(Product, id=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def CreateProduct(request):
    product = ProductSerializer(data=request.data)

    if product.is_valid():
        product.save()
        return Response(product.data)
    return Response(product.errors)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsAdminUser])
def UpdateProduct(request, id):
    product = get_object_or_404(Product, id=id)
    serializer = ProductSerializer(instance=product, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def DeleteProduct(request, id):
    product = get_object_or_404(Product, id=id)
    deleted = product.delete()
    return Response({'message': f'product <id:{id}> deleted'}, status=status.HTTP_204_NO_CONTENT)


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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateReview(request, product_id):
    user = get_object_or_404(User, username=request.user.username)
    
    data = request.data.dict()
    data.update({'user_id': user.id, 'product_id': product_id})

    reviews = ReviewSerializer(data=data)

    if reviews.is_valid():
        reviews.save()
        return Response(reviews.data, status=status.HTTP_201_CREATED)
    return Response(reviews.errors)


### ORDER SECTION ###
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ListOrders(request):
    user_id = get_object_or_404(User, id=request.user.id)
    orders = Order.objects.filter(user_id=user_id)
    queryset = OrderSerializer(orders, many=True)
    return Response(queryset.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateOrder(request, product_id):
    user = get_object_or_404(User, id=request.user.id)
    product = get_object_or_404(Product, id=product_id)
    units = request.POST.get('units')

    if units:
        total_amount = product.price * int(units)
        data = request.data.dict()
        data.update({'user_id': user.id, 'product_id': product.id, 'units': int(units), 'total_amount': total_amount})

        order = OrderSerializer(data=data)
        
        if order.is_valid():
            order.save()
            return Response({'message': 'order placed successfully!'})
        return Response(order.errors)
    return Response({'message': 'units required'}, status=status.HTTP_400_BAD_REQUEST)