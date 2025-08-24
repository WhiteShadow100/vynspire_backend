from django.http import JsonResponse
from .models import User
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import authenticate
from django.conf import settings
import datetime
import jwt


# secret key for token
SECRET_KEY = settings.SECRET_KEY


@csrf_exempt
def register(request ):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # parse JSON body
            username = data.get("username")
            password = data.get("password")
            email = data.get("email", "")

            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already exists"}, status=400)

            user = User.objects.create_user(username=username, password=password, email=email)
            return JsonResponse({"message": "User created successfully", "user_id": user.id})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Only POST method allowed"}, status=405)


@csrf_exempt
def login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            user = authenticate(username=username, password=password)
            
            if user is not None:
                # Create JWT token
                payload = {
                    "user_id": user.id,
                    "username": user.username,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
                }
                
                token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
                return JsonResponse({"token": token})

            else:
                return JsonResponse({"error": "Invalid credentials", "message": "Invalid Credential."}, status=401)
        except Exception as e:
            return JsonResponse({"error": str(e), "message": str(e)}, status=400)

    return JsonResponse({"error": "Only POST method allowed"}, status=405)
