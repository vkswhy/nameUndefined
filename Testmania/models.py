from django.db import models

# Create your models here.
class Contests(models.Model){
    contestName=models.CharField(max_length=50)
}
