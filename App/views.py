from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User

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
