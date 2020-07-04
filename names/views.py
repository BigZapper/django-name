from django.shortcuts import render, redirect
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

from django.contrib.auth import get_user_model, login
from django.contrib.auth.forms import AuthenticationForm
import requests, json

from rest_framework.pagination import PageNumberPagination


def get_paginated_queryset_response(query_set, request):
    paginator = PageNumberPagination()
    paginator.page_size = 20
    paginated_qs = paginator.paginate_queryset(query_set, request)
    serializer = NameSerializer(paginated_qs, many=True, context={'request':request})
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET', 'POST', 'DELETE'])
def name_list(request):
    # GET danh sách các name, 
    if request.method == 'GET':
        names = Name.objects.all()
        # print(names)
        lastname = request.GET.get('lastname', None)
        if lastname is not None:
            print(request.GET)
            names = names.filter(lastname__icontains=lastname).order_by('lastname')
        
        names_serializer = NameSerializer(names, many=True)
        return JsonResponse(names_serializer.data, safe=False)
        # return get_paginated_queryset_response(names, request)

    # POST một name mới
    elif request.method == 'POST':
        name_data = JSONParser().parse(request)
        user = Name.objects.create(id=request.data.get('id'),fullname=request.data.get('fullname'),menh=request.data.get('menh'),van=request.data.get('van'),
        gioitinh=request.data.get('gioitinh'),lastname=request.data.get('lastname'),meaning=request.data.get('meaning'),likes=request.data.get('likes'))
        print(user.fullname)
        name_serializer = NameSerializer(data=name_data)
        if name_serializer.is_valid():
            name_serializer.save()
            return JsonResponse(name_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(name_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE toàn bộ name
    # elif request.method == 'DELETE':
    #     count = Name.objects.all().delete()
    #     return JsonResponse({'message': '{} Names were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def name_detail(request, pk):
    if request.user.is_authenticated:
            
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
                    return JsonResponse(name_serializer.data, status=status.HTTP_200_OK)
                return JsonResponse(name_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            #Xoá một name theo id
            elif request.method == 'DELETE':
                name.delete()
                return JsonResponse({'message': 'Name was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

        except Name.DoesNotExist: 
            return JsonResponse({'message': 'The name does not exist'}, status=status.HTTP_404_NOT_FOUND)
    return redirect('login/')
    
 

@api_view(['GET'])
def view_name_list(request):
    names = Name.objects.filter(lastname__icontains=request.GET.get('lastname', '')).filter(menh__icontains=request.GET.get('menh', '')).filter(Q(gioitinh=request.GET.get('gioitinh', '')) | Q(gioitinh='Chung')).order_by('lastname')
    print(request.GET)
    if request.method == 'GET': 
        names_serializer = NameSerializer(names, many=True)
        return JsonResponse(names_serializer.data, safe=False)


@api_view(['GET'])
def view_name_list_2(request):
    tencha = request.GET.get('tencha', '')
    tenme = request.GET.get('tenme', '')
    menhCha = Name.objects.filter(lastname__icontains=tencha).values('menh').first()
    menhCha=menhCha['menh']
    if tencha != "":
        names = Name.objects.filter(menh__icontains=menhCha).filter(Q(gioitinh=request.GET.get('gioitinh', '')) | Q(gioitinh='Chung')).order_by('lastname')
    elif tencha == "":
        menhMe = Name.objects.filter(lastname__icontains=request.GET.get('tenme', '')).values('menh').first()
        menhMe=menhMe['menh']
        names = Name.objects.filter(menh__icontains=menhMe).filter(Q(gioitinh=request.GET.get('gioitinh', '')) | Q(gioitinh='Chung')).order_by('lastname')
    else:
        random_idx = random.randint(0, Name.objects.count() - 1)
        names = Name.objects.all()[random_idx]
    if request.method == 'GET': 
        names_serializer = NameSerializer(names, many=True)
        return JsonResponse(names_serializer.data, safe=False)

@api_view(['POST'])
def like_name(request, pk):
    name = Name.objects.get(pk=pk) 
    if request.method == 'POST':
        name = Name.objects.get(id=pk)
        name.likes += 1
        name.save()
        name_serializer = NameSerializer(name)
        return JsonResponse(name_serializer.data, status=status.HTTP_200_OK)
        
@api_view(['GET'])
def top_like(request):
    names = Name.objects.order_by('-likes').filter()[:10]
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
    tmp = content.split("<p class=\"lvn-xemntx-colorred\">")
    line1 = re.sub("<.*?>", "", tmp[1])
    line2 = re.sub("<.*?>", "", tmp[2])
    line3 = re.sub("<.*?>", "", tmp[3])
    line4 = re.sub("<.*?>", "", tmp[4])
    line5 = re.sub("<.*?>", "", tmp[5])
    responseData = {
        'name': line1,
        'overview': line2,
        'job':line3,
        'characteristic': line4,
        'love': line5,
    }
    # non_empty_lines = [line for line in lines if line.strip() != ""]
    # string_without_empty_lines = ""
    # for line in non_empty_lines:
    #     string_without_empty_lines += line + "\n"
    
    return JsonResponse(responseData, status=status.HTTP_200_OK)

def test(request):
    print(request.body)
    print(json.loads(request.body))
    x = json.loads(request.body)
    print(x['fullname'])
    return HttpResponse('Oke')

User=get_user_model()
def create_user(request):
    username = 'jingkoo'
    password = '12345'
    user = User.objects.create_user(username=username,password=password)
    user.save()
    return HttpResponse("oke")

def login_user(request):
    if request.user.is_authenticated:
        return redirect('/api/names/')
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        user=form.get_user()
       
        print(request.user)
        res = request.POST["g-recaptcha-response"]
        secretKey = '6LcO9KcZAAAAAOEqk4Gcv10A0v9xJ18oMz2P3a63'
        data = {
            "secret":secretKey,
            "response":res
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        response = json.loads(r.text)
        result = response["success"]
        print("message: ", result)
        if result:
            login(request, user)
            return redirect('/api/names/')
        return render(request,'form.html',{"form":form})
    return render(request,'form.html',{"form":form})