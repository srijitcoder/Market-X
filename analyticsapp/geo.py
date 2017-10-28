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

from .models import Doctor, Hospital, Disease
from .serializers import DoctorSerializer, DiseaseSerializer, Disease1Serializer



def get_sub_locality(address):


    sensor = 'true'

    base = "http://maps.googleapis.com/maps/api/geocode/json?"

    params = "address={address}&sensor={sen}".format(address=address,sen=sensor)
    url = "{base}{params}".format(base=base, params=params)
    response = requests.get(url).json()
    print(response)



'''
latitude = 28.6884549
longitude = 77.1757503

error = True

while(error):
    try:
        get_sub_locality(latitude, longitude)
        error = False
    except:
        error = True


'''

