from django.shortcuts import render,HttpResponse
from .forms import registerForm
def homePage(request):
    return render(request,'base.html')
def register(request):
    if request.method=="POST":
        form=registerForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            return HttpResponse(request,"user is valid")
        else:
            return render(request,'register.html',{'form':form})
    else:
        form=registerForm()
        return render(request,'register.html',{'form':form})
