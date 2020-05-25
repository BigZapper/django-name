from django.shortcuts import render
from django.db.models import Q
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from django.http.response import HttpResponse
 
from names.models import Name
from names.serializers import NameSerializer
from rest_framework.decorators import api_view
from bs4 import BeautifulSoup
import urllib.request
from urllib.request import urlopen, Request
import urllib.parse
import re

@api_view(['GET', 'POST', 'DELETE'])
def name_list(request):
    # GET danh sách các name, 
    if request.method == 'GET':
        names = Name.objects.all()
        
        lastname = request.GET.get('lastname', None)
        if lastname is not None:
            print(request.GET)
            names = names.filter(lastname__icontains=lastname).order_by('lastname')
        
        names_serializer = NameSerializer(names, many=True)
        return JsonResponse(names_serializer.data, safe=False)

    # POST một name mới
    elif request.method == 'POST':
        name_data = JSONParser().parse(request)
        name_serializer = NameSerializer(data=name_data)
        if name_serializer.is_valid():
            name_serializer.save()
            return JsonResponse(name_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(name_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE toàn bộ name
    elif request.method == 'DELETE':
        count = Name.objects.all().delete()
        return JsonResponse({'message': '{} Names were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def name_detail(request, pk):
    # Tìm các names theo pk (id)
    try: 
        name = Name.objects.get(pk=pk) 

        #Tìm một name theo id
        if request.method == 'GET':
            name_serializer = NameSerializer(name)
            return JsonResponse(name_serializer.data)

        #Update một name theo id
        elif request.method == 'PUT':
            name_data = JSONParser().parse(request)
            name_serializer = NameSerializer(name, data=name_data)
            if name_serializer.is_valid():
                name_serializer.save()
                return JsonResponse(name_serializer.data)
            return JsonResponse(name_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        #Xoá một name theo id
        elif request.method == 'DELETE':
            name.delete()
            return JsonResponse({'message': 'Name was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

    except Name.DoesNotExist: 
        return JsonResponse({'message': 'The name does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 

@api_view(['GET'])
def view_name_list(request):
    names = Name.objects.filter(lastname__icontains=request.GET.get('lastname', '')).filter(menh__icontains=request.GET.get('menh', '')).filter(Q(gioitinh=request.GET.get('gioitinh', '')) | Q(gioitinh='Chung')).order_by('lastname')
    print(request.GET)
    if request.method == 'GET': 
        names_serializer = NameSerializer(names, many=True)
        return JsonResponse(names_serializer.data, safe=False)



@api_view(['GET'])
def meaning_name(request):
    name=request.GET.get('name','')
    print(urllib.parse.quote(name))
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    reg_url = 'https://lichvannien365.com/boi-ten?fullname='+urllib.parse.quote(name)
    req = Request(url=reg_url, headers=headers) 
    page = urllib.request.urlopen(req)
    soup = BeautifulSoup(page, 'html.parser')
    content = str(soup.find('div', class_='lvn-xoneday-block'))
    # lines = re.sub("<.*?>", "", content).split("\n")
    # non_empty_lines = [line for line in lines if line.strip() != ""]
    # string_without_empty_lines = ""
    # for line in non_empty_lines:
    #     string_without_empty_lines += line + "\n"
    return HttpResponse(content)