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

from .serializers import DoctorSerializer, RetailerSerializer, Retailer1Serializer

from django.db.models import Count



def get_sub_locality(latitude,longitude):


    sensor = 'true'

    base = "http://maps.googleapis.com/maps/api/geocode/json?"

    params = "latlng={lat},{lon}&sensor={sen}".format(lat=latitude,lon=longitude,sen=sensor)
    url = "{base}{params}".format(base=base, params=params)
    response = requests.get(url).json()
    print(response['results'][0]['address_components'])

    for  item in response['results'][0]['address_components']:
        for categ in item['types']:
            if 'sublocality' or 'sublocality_level_2' or 'sublocality_level_3' in categ:
                print(item['short_name'])
                return item['short_name']  



@api_view(['GET', 'POST', ])
def get_total_my(request):

	try:
		my_count = Retailer.objects.filter(Retailer_name=request.POST['Retailer']).count()
		return JsonResponse({'count': my_count})
	except Exception as e:
		return JsonResponse({'error': str(e)})


@api_view(['GET', 'POST', ])
def get_Retailer_distribution(request):

	q = Retailer.objects.filter(Retailer_name=request.POST['Retailer_name'].lower()).values('place').annotate(total=Count('place'))

	data = []
	for my in q:
		print(my['place'])
		temp = Retailer.objects.filter(place=my['place'])[0]
		#print(temp.lat, temp.lon)
		#print(my)
		data.append(
			{'center' : { 'lat':float(temp.lat) ,  'lng': float(temp.lon) },'population': my['total']*69, 'place': my['place']
			 
			  }
			)
		print(data)

	return JsonResponse(data,safe=False)
	#return JsonResponse([{'population': 100000, 'center': {'lat': 28.688, 'lng': 77.176}, 'place': 'ashok vihar'}, {'population': 50000, 'center': {'lat': 28.525, 'lng': 77.207}, 'place': 'saket'}],safe=False)


@api_view(['GET', 'POST', ])
def date_filter(request):

	try:
		from_date = request.POST['from_date']
		to_date = request.POST['to_date']

		dis_dic = {}
		q = Retailer.objects.filter(date_time__range=[from_date, to_date]).values('Retailer_name').annotate(total=Count('Retailer_name'))
		for item in q:
			dis_dic[item['Retailer_name']] = item['total']
		return JsonResponse(dis_dic)
	except Exception as e:
		return JsonResponse({'error': str(e)})


@api_view(['GET', 'POST', ])
def date_filter_by_locality(request):

	try:
		from_date = request.POST['from_date']
		to_date = request.POST['to_date']
		place = request.POST['place']

		dis_dic = {}
		q = Retailer.objects.filter(date_time__range=[from_date, to_date], place=place).values('Retailer_name').annotate(total=Count('Retailer_name'))
		for item in q:
			dis_dic[item['Retailer_name']] = item['total']
		return JsonResponse(dis_dic)
	except Exception as e:
		return JsonResponse({'error': str(e)})



@api_view(['GET', 'POST', ])
def date_filter_by_Retailer(request):

	try:
		from_date = request.POST['from_date']
		to_date = request.POST['to_date']
		Retailer_name = request.POST['Retailer_name']

		dis_dic = {}
		q = Retailer.objects.filter(date_time__range=[from_date, to_date], Retailer_name=Retailer_name).values('place').annotate(total=Count('place'))
		for item in q:
			dis_dic[item['place']] = item['total']
		return JsonResponse(dis_dic)
	except Exception as e:
		return JsonResponse({'error': str(e)})


@api_view(['GET', 'POST', ])
def time_series_plot(request):
	
	from_date = request.POST['from_date']
	to_date = request.POST['to_date']
	Retailer_name = request.POST['Retailer_name']

	X = []
	Y = []

	q = Retailer.objects.filter(date_time__range=[from_date, to_date], Retailer_name=Retailer_name).values('date_time').annotate(total=Count('date_time'))
	for item in q:
		X.append(item['date_time'].strftime('%d-%m-%Y'))
		Y.append(item['total'])

	return JsonResponse({'X':str(X), 'Y':str(Y)})
	


@api_view(['GET', 'POST', ])
def time_series_plot_by_locality(request):
	
	from_date = request.POST['from_date']
	to_date = request.POST['to_date']
	Retailer_name = request.POST['Retailer_name']
	place = request.POST['place']

	X = []
	Y = []

	q = Retailer.objects.filter(date_time__range=[from_date, to_date], Retailer_name=Retailer_name, place=place).values('date_time').annotate(total=Count('date_time'))
	for item in q:
		X.append(item['date_time'].strftime('%d-%m-%Y'))
		Y.append(item['total'])

	return JsonResponse({'X':str(X), 'Y':str(Y)})


@api_view(['GET', 'POST', ])
def quant_analysis(request):
	place = request.POST['place']
	
	result = {}

	#total_my_count = Retailer.objects.filter(place=place).count()

	diseses = Retailer.objects.values('Retailer_name').distinct()
	print(diseses)

	#total_mys = Retailer.objects.filter().count()
	#q_local = Retailer.objects.filter(place=place).values('Retailer_name').annotate(total=Count('Retailer_name'))


	for item in diseses:
		q_net = Retailer.objects.filter(Retailer_name=item['Retailer_name']).values('Retailer_name').annotate(total=Count('Retailer_name'))
		place_dis_count = Retailer.objects.filter(Retailer_name=item['Retailer_name'], place=place).values('Retailer_name').annotate(total=Count('Retailer_name'))
		#print(item['Retailer_name'])
		#print(q_net)
		print(place_dis_count)
		#print(place_dis_count[0]['total']/q_net[0]['total'])
		result[item['Retailer_name']] = (place_dis_count[0]['total']/q_net[0]['total'])*100

	return JsonResponse({'data':result})



@api_view(['GET', 'POST', ])
def locality_analysis(request):
	place = request.POST['place']
	
	data = []

	total_my_count = Retailer.objects.filter(place=place).count()

	diseses = Retailer.objects.values('Retailer_name').distinct()
	q_local = Retailer.objects.filter(place=place).values('Retailer_name').annotate(total=Count('Retailer_name'))
	print(total_my_count)
	
	for item in q_local:
		data.append({ item['Retailer_name'] : (item['total']/total_my_count)*100 })

	return JsonResponse({'data':data})


@api_view(['GET', 'POST', ])
def locality__analysis_2(request):
	place = request.POST['place']
	from_date = request.POST['from_date']
	to_date = request.POST['to_date']
	
	data = []

	total_my_count = Retailer.objects.filter(date_time__range=[from_date, to_date], place=place).count()

	diseses = Retailer.objects.values('Retailer_name').distinct()
	q_local = Retailer.objects.filter(date_time__range=[from_date, to_date], place=place).values('Retailer_name').annotate(total=Count('Retailer_name'))
	print(total_my_count)
	
	for item in q_local:
		data.append({ item['Retailer_name'] : (item['total']/total_my_count)*100 })

	return JsonResponse({'data':data})