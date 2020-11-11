from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .forms import registerForm,loginForm,createTestModelForm,createQuestionModelForm
from .models import Contests,Questions

def homePage(request):
    auth=False
    if request.user.is_authenticated:
        auth=True
    return render(request,'index.html',{'a':auth,'username':request.user.username,'info':"in the home page"})

def registerView(request):
    
    if request.method=="POST":
        form=registerForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            login(request,user)
            return redirect('/',{'info':"Registration Successful"})
        else:
            return render(request,'register.html',{'form':form})
    else:
        form=registerForm()
        return render(request,'register.html',{'form':form})

def loginView(request):
    if request.method=="POST":
        form=loginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']

            user=authenticate(request,username=username,
            password=password)
            print("here",user)
            if user is not None:
                login(request,user)
                return redirect("/")
            else:
                return render(request,"login.html",{"form":form,"info":"incorrect username or password"})
        else:
            return render(request,"login.html",{"form":form,"info":"login failed due to form is not valid"})
    else:
        form=loginForm()
        return render(request,"login.html",{"form":form,"info":"please input the details to login"})

def logoutView(request):
    logout(request)
    return redirect('/')

@login_required
def createTestView(request):
    if request.method=="POST":
        form=createTestModelForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            contest=form.save(commit=False)
            contest.Author=request.user
            print(request.user)
            contest.save()
            form=createQuestionModelForm()
            return render(request,"createQuestion.html",{'form':form,'noOfQues':contest.noOfQues,"qNo":1,'contestId':contest.id})
        else:
            print(form.errors)
            return redirect("/")
    else:
        form=createTestModelForm()
        print(form)
        return render(request,"createTest.html",{'form':form})


@login_required
def takeTestView(request):
    if request.method=='POST':
        id=request.POST.get('id')
        query_set=Contests.objects.filter(pk=id)
        if query_set.count()>0:
            return HttpResponse('SUCCess')
        else:
            return HttpResponse('ERRor')
        return HttpResponse('success')
    return render(request,'takeTest.html')
    
    

def createQuestionView(request):
    contestId=request.POST.get("contestId")
    contest=Contests.objects.get(pk=contestId)
    if contestId is None:
        redirect('/')
    if request.user is not contest.Author:
        redirect('/')
    
    if request.method=="POST":
        form=createQuestionModelForm(request.POST)
        ques=form.save(commit=False)

        ques.contest=contest
        ques.save()
        


        qNo=int(request.POST.get("qNo"))+1
        form=createQuestionModelForm()

        if qNo > contest.noOfQues:
            return redirect("/")
        return render(request,"createQuestion.html",{'form':form,'noOfQues':contest.noOfQues,"qNo":qNo,'contestId':contest.id})
    else:
        form=createQuestionModelForm()
        return render(request,"createQuestion.html",{'form':form,'noOfQues':contest.noOfQues,"qNo":1,'contestId':contest.id})

