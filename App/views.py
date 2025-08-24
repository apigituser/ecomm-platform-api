from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from .models import Product, Order
from django.contrib.auth.models import User

class UserRegistration(APIView):
    
    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")

        if username and password and email:
            user = User.objects.create_user(username, password, email)
            if user is not None:
                return JsonResponse({"status": "registeration successful"})
            return JsonResponse({"status": "user not registered"}, status=400)
        return JsonResponse({"status": "username, password and email are required"}, status=400)
