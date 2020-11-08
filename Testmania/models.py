from django.db import models


class Contests(models.Model):
    contestName=models.CharField(max_length=50)
class Questions(models.Model):
    question=models.CharField(max_length=200)
    optionA=models.CharField(max_length=50)
    optionB=models.CharField(max_length=50)
    optionC=models.CharField(max_length=50)
    optionD=models.CharField(max_length=50)
    contest=models.ForeignKey(Contests,on_delete=models.CASCADE)
