from django import forms
from .models import Contests
from django.contrib.auth.models import User
class registerForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password']
        
class loginForm(forms.Form):
    username=forms.CharField(max_length=15,required=True)
    password=forms.CharField(max_length=15,required=True)


class createTestModelForm(forms.ModelForm):
    class Meta:
        model=Contests
        fields=['contest','noOfQues','startDate','startTime','endDate','endTime','timePerQues']
