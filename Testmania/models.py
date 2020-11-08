from django.db import models
class Questions(models.model):
    question=models.CharField(max_length=200)
    optionA=models.CharField(max_length=100)
    optionB=models.CharField(_(""), max_length=50)
# Create your models here.
class Contests(models.Model){
    contestName=models.CharField(max_length=50)
}

