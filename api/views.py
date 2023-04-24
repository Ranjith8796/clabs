import json
import random
import string
import requests
from django.shortcuts import render
from django.http import JsonResponse
from .models import account, destination
from .serializers import accountserializer, destinationserializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def account_list(request):
    if request.method == 'GET':
        acc = account.objects.all()
        serializer = accountserializer(acc, many=True)
        return Response({"accounts": serializer.data})

    elif request.method == 'POST':
        val = request.data
        val["token"] = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
        serializer = accountserializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        val = account.objects.get(pk=request.data["account_id"])
        serializer = accountserializer(val, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            val = account.objects.get(pk=request.data["account_id"])
            val.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except account.DoesNotExist:
            return Response({"Response":"Invalid Account id"}, status=status.HTTP_404_NOT_FOUND)
        
        


@api_view(['GET'])
def account_info(request, id):
    try:
        val = account.objects.get(pk=id)
    except account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = accountserializer(val)
    return Response(serializer.data)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def dest_list(request):
    if request.method == 'GET':
        acc = destination.objects.all()
        serializer = destinationserializer(acc, many=True)
        return Response({"destination": serializer.data})

    elif request.method == 'POST':
        serializer = destinationserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        val = destination.objects.get(pk=request.data["id"])
        serializer = destinationserializer(val, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            val = destination.objects.get(pk=request.data["id"])
            val.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except destination.DoesNotExist:
            return Response({"Response":"Invalid Destination id"}, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@require_http_methods(["POST"])
def data_handler(request):

    try:
        json_data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"Response":"Invalid Data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        header_data = request.headers["CL-X-TOKEN"]
        val = account.objects.get(token = header_data)
    except account.DoesNotExist:
        return JsonResponse({"Response":"Un Authenticate"}, status=status.HTTP_404_NOT_FOUND)
    except KeyError:
        return JsonResponse({"Response":"Un Authenticate"}, status=status.HTTP_404_NOT_FOUND)

    acc_id = val.account_id
    dest = destination.objects.filter(account_id = acc_id)

    def call_dest(dest):
        if dest.http_method == "GET":
            url = dest.distination_url
            r = requests.get(url, params=json_data)
            return r.json()
        if dest.http_method == "POST":
            url = dest.distination_url
            header = dest.headers
            r = requests.post(url = url, json = json_data, headers = header)
            return r.json()
        
    resp = {i.distination_url :call_dest(i) for i in dest}
    return JsonResponse(resp, status=status.HTTP_200_OK)
    
    