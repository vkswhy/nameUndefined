from django import forms
from .models import Contests,Questions
from django.contrib.auth.models import User


inputDateFormat=[   '%Y-%m-%d',      # 2006-10-25
                    '%m/%d/%Y',       #10/25/2006
                    '%m/%d/%y']       # 10/25/06
class inputDate(forms.DateInput):
    input_type='date'
class inputTime(forms.TimeInput):
    input_type='time'

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
        widgets={
            'startDate':inputDate(),
            'endDate':inputDate(),
            'startTime':inputTime(),
            'endTime':inputTime(),   
        }

class createQuestionModelForm(forms.ModelForm):
    class Meta:
        model=Questions
        fields=['question','optionA','optionB','optionC','optionD','answer']
