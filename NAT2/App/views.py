from django.shortcuts import render
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
import json
from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import CustomToken
from uuid import uuid4
import uuid
from django.contrib.auth.models import User
from django.utils import timezone


# Create your views here.

@csrf_exempt
def login(request):
    if request.method == 'POST':
        if not request.body:
            return JsonResponse({'error': 'Required username and password'}, status=401)

        request_body = request.body
        json_data = request_body.decode('utf-8')
        data = json.loads(json_data)
        username = data["username"]
        password = data["password"]
        user = authenticate(username=username, password=password)

        if not user:
            return JsonResponse({'error': 'Invalid username or password'}, status=401)

        if CustomToken.objects.filter(user=username).exists():
            my_object = CustomToken.objects.get(user=username)
            exptime = my_object.expires_at
            if exptime > timezone.now():
                token = CustomToken.objects.filter(
                    user=username).values('token_key').first()
                token_key = token['token_key']
                return JsonResponse({'msg': 'Token Already Exists', 'Token': token_key}, status=200)
            else:
                my_object.delete()
                token_key = str(uuid.uuid4())
                user = User.objects.get(username=user.username)
                print(user)
                token = CustomToken(user=user, token_key=token_key)
                token.save()
                return JsonResponse({'Bearer': username, 'token': token_key}, status=200)

        else:
            token_key = str(uuid.uuid4())
            user = User.objects.get(username=user.username)
            print(user)
            token = CustomToken(user=user, token_key=token_key)
            token.save()
            return JsonResponse({'Bearer': username, 'token': token_key}, status=200)
    else:
        return JsonResponse({'error': 'Unsupported request method'}, status=405),


def show_user_data(request):
    if request.method == 'GET':
        user = request.headers.get('Username')
        token = request.headers.get('Authorization')

        if user is not None and token is not None:
            if CustomToken.objects.filter(user=user).exists():
                userobject = CustomToken.objects.get(user=user)
                if userobject.token_key == token:
                    exptime = userobject.expires_at
                    if exptime > timezone.now():
                        data = User.objects.all()
                        return JsonResponse({'Users': list(data.values())}, status=200)
                    else:
                        return JsonResponse({"Msg": "Token Expired"}, status=400)
                else:
                    return JsonResponse({'Msg': 'User and token mismatched'}, status=400)
            else:
                return JsonResponse({'Msg': 'Invalid User'}, status=400)

        else:
            return JsonResponse({'Msg': 'Username and Token required'}, status=400)

    else:
        return JsonResponse({'Msg': 'Invalid Request'}, status=400)


def logout(request):
    if request.method == 'GET':
        user = request.headers.get('Username')
        token = request.headers.get('Authorization')

        if user is not None and token is not None:
            if CustomToken.objects.filter(user=user).exists():
                logoutobject = CustomToken.objects.get(user=user)
                if logoutobject.token_key == token:
                    logoutobject.delete()
                    return JsonResponse({'Status': 'Logout', 'Token Removed': token}, status=400)
                else:
                    return JsonResponse({'Msg': 'User and token mismatched'}, status=400)
            else:
                return JsonResponse({'Msg': 'Invalid User'}, status=400)

        else:
            return JsonResponse({'Msg': 'Username and Token required'}, status=400)

    else:
        return JsonResponse({'Msg': 'Invalid Request'}, status=400)
