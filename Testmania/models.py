from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class Contests(models.Model):
    contest=models.CharField(blank=True,max_length=50,default=None)
    Author=models.ForeignKey(User, on_delete=models.CASCADE,blank=True)
    noOfQues=models.IntegerField(blank=True,default=None)
    startDate=models.DateField()
    startTime=models.TimeField()
    endDate=models.DateField()
    endTime=models.TimeField()
    timePerQues=models.CharField(blank=True,max_length=12,default=None)
    
class Questions(models.Model):
    question=models.CharField(blank=True,max_length=200,default=None)
    optionA=models.CharField(blank=True,max_length=50,default=None)
    optionB=models.CharField(blank=True,max_length=50,default=None)
    optionC=models.CharField(blank=True,max_length=50,default=None)
    optionD=models.CharField(blank=True,max_length=50,default=None)
    contest=models.ForeignKey(Contests,on_delete=models.CASCADE)
    answer=models.CharField(blank=True,max_length=5,default=None)
    responseA=models.ManyToManyField(User,related_name="response_a")
    responseB=models.ManyToManyField(User,related_name="response_b") 
    responseC=models.ManyToManyField(User,related_name="response_c") 
    responseD=models.ManyToManyField(User,related_name="response_d") 

admin.site.register(Contests)
admin.site.register(Questions)
