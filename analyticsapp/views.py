from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from oauth2_provider.decorators import protected_resource

# Create your views here.

from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from oauth2_provider.models import AccessToken

import requests
from django.conf import settings
import json

from .serializers import RetailerSerializer, RetailerSerializer, Retailer1Serializer

from django.db.models import Count



def get_retailer(username,password):
	
	vend_name = Retailer.objects.get(username=username, password=password)

	d_name = vend_name.name
	h_add = vend_name.sect

	return d_name,h_add



def validate_request(username, password):
	if Retailer.objects.filter(username=username, password=password).exists():
		return True
	else:
		return False


@api_view(['GET', 'POST', ])
def register_product(request):

	username = request.POST['username']
	password = request.POST['password']
	prod_cat = request.POST['prod_cat'].lower()
	lat = request.POST['lat']
	lon = request.POST['lon']
	place = request.POST['place']

	if validate_request(username, password):
		prod_cat = Retailer.objects.get(username=username,password=password)
		
		d_name, h_name = get_hospital(username, password)

		dis_instande = Retailer(h_name=h_name, product_cat=product_cat,lon=lon, lat=lat,place=place)
		dis_instande.save()
		return JsonResponse({'status': True})



@api_view(['GET', 'POST', ])
def login_usr(request):

	try:
		doc_quer = Retailer.objects.filter(username= request.POST['username'], password=request.POST['password'])
		serializer = RetailerSerializer(doc_quer, many=True, context={'request': request})
		return JsonResponse(serializer.data, safe=False)
	
	except Exception as e:
		return JsonResponse({'error': str(e)})



@api_view(['GET', 'POST', ])
def custom_plot(request):
	
		try:
			Retailer_name = request.POST['prod'].lower()
			place = request.POST['place']
			lat = request.POST['lat']
			lon = request.POST['lng']

			if Retailer_name and place:
				dis_count = Retailer.objects.filter(Retailer_name= Retailer_name, place=place).count()
				#return JsonResponse({'population': dis_count})
				return JsonResponse({'center' : { 'lat':float(lat) ,  'lng': float(lon) },'population':dis_count*69, 'place': place})		

		except Exception as e:
			return JsonResponse({'error':str(e)})




@api_view(['GET', 'POST', ])
def plot_by_place(request):
	
		try:
			place_dic = {}
			place = request.POST['place']
			res = Retailer.objects.filter(place=place).values('Retailer_name').annotate(total=Count('Retailer_name'))
			for item in res:
				place_dic[item['Retailer_name']] = item['total']
			return JsonResponse(place_dic)

		except Exception as e:
			return JsonResponse({'error':str(e)})


@api_view(['GET', 'POST', ])
def plot_by_Retailer(request):
	
		try:
			place_dic={}
			Retailer_name = request.POST['Retailer_name']
			res = Retailer.objects.filter(Retailer_name=Retailer_name).values('place').annotate(total=Count('place'))
			for item in res:
				place_dic[item['place']] = item['total']
			return JsonResponse(place_dic)

		except Exception as e:
			return JsonResponse({'error':str(e)})