from django.db import models

class Questions(models.model):
    question=models.CharField(max_length=200)



