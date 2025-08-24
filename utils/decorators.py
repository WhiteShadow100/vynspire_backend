from functools import wraps
from django.http import HttpResponse, JsonResponse, Http404
import jwt
from django.conf import settings


# secret key for token
SECRET_KEY = settings.SECRET_KEY

def jwt_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JsonResponse({"error": "Authorization header missing or invalid"}, status=401)

        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token expired"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Invalid token"}, status=401)

        # Attach user info to request
        request.user_id = payload.get("user_id")
        request.username = payload.get("username")

        return view_func(request, *args, **kwargs)
    return wrapper
