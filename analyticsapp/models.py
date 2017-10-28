from django.db import models
from datetime import datetime    




class Retailer(models.Model):

	name = models.CharField(max_length=100, primary_key=True)
	address = models.CharField(max_length=100)
	sector_choices = (('a','Private'),('b','Government'),('c','Semi-Private'),('d','Other'))
	sector = models.CharField(max_length=1, choices=sector_choices)

	class Meta:
		unique_together = (("name","address"),)


	def __str__(self):
		return self.name



class Outlet(models.Model):

	username = models.CharField(max_length=50, primary_key=True)
	password = models.CharField(max_length=50)
	name = models.CharField(max_length=100)
	category = models.CharField(max_length=100)
	address = models.CharField(max_length=100)

	def __str__(self):


		return self.name