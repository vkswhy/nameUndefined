from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .forms import registerForm,loginForm,createTestModelForm,createQuestionModelForm,updateProfileForm
from .models import Contests,Questions
from random import randint
#To display Home Page
def homePage(request):
    auth=False
    if request.user.is_authenticated:
        auth=True
    return render(request,'index.html',{'a':auth,'username':request.user.username,'info':"in the home page"})

#To display Registration Page
def registerView(request):
    if request.user.is_authenticated:
        return redirect("/")
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


#To display login Page
def loginView(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method=="POST":
        form=loginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']

            user=authenticate(request,username=username,
            password=password)
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


#To display logout Page
@login_required
def logoutView(request):
    logout(request)
    return redirect('/')


#To display create test Page
@login_required
def createTestView(request):
    if request.method=="POST":
        form=createTestModelForm(request.POST)
        if form.is_valid():
            contest=form.save(commit=False)
            contest.Author=request.user
            contest.save()
            form=createQuestionModelForm()
            return render(request,"createQuestion.html",{'form':form,'noOfQues':contest.noOfQues,"qNo":1,'contestId':contest.id,'a':True,'username':request.user.username})
        else:
            return redirect("/")
    else:
        form=createTestModelForm()
        print(form)
        return render(request,"createTest.html",{'form':form})
        return render(request,"createTest.html",{'form':form,'a':True,'username':request.user.username})


#To display take test Page
@login_required
def takeTestView(request):
    
    if request.method=='POST':
        id=request.POST.get('id')
        query_set=Contests.objects.filter(pk=id)
        if query_set.count()>0:
            questDetail=displayUtil(request,query_set[0])
            if questDetail is None:
                return HttpResponse("Submitted")
            questDetail.update(getUser(request))
            query_set[0].participants.add(request.user)
            return render(request,"displayQuestion.html",questDetail)
        else:
            return HttpResponse('ERRor')
    return render(request,'takeTest.html',{'a':True,'username':request.user.username})
    
    
#for create Question Page
@login_required
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
        return render(request,"createQuestion.html",{'form':form,'noOfQues':contest.noOfQues,"qNo":qNo,'contestId':contest.id,'a':True,'username':request.user.username})
    else:
        form=createQuestionModelForm()
        return render(request,"createQuestion.html",{'form':form,'noOfQues':contest.noOfQues,"qNo":1,'contestId':contest.id})
@login_required
def profileView(request):
    if request.method=='POST':
        try:
            form=updateProfileForm(request.POST,request.FILES,instance=request.user.profile)
            # print('hello already user')
            form.save()
        except:
            form=updateProfileForm(request.POST,request.FILES)
            profile=form.save()
            profile.user=request.user
            profile.save()
        return redirect('/')
    else:
        form=updateProfileForm()
        return render(request,'profile.html',{'form':form})
#for display questions
@login_required
def displayQuesView(request):
    if request.method=="POST":
        quesId=request.POST.get('quesId')
        contestId=request.POST.get('contestId')
        option=request.POST.get('option')
        q=Questions.objects.get(pk=quesId)
        if option=='A':
            q.responseA.add(request.user)
        elif option=='B':
            q.responseB.add(request.user)
        elif option=='C':
            q.responseC.add(request.user)
        else:
            q.responseD.add(request.user)
        q.save()
        
        contest=Contests.objects.get(pk=contestId)
        questDetail=displayUtil(request,contest)
        
        if questDetail is None:
            return HttpResponse("Thank You")
        questDetail.update(getUser(request))
        return render(request,"displayQuestion.html",questDetail)


    else:

        return redirect('/takeTest/')
        

@login_required
def dashboardView(request):
    form=getUser(request)
    form.update({"contestCreated":contestCreatedDetails(request)})
    form.update({"contestTaken":contestTakenDetails(request)})

    return render(request,"dashboard.html",form)

#utility function to display a question
def displayUtil(request,contestobj):
    questionSet=Questions.objects.filter(contest=contestobj).exclude(responseA=request.user).exclude(responseB=request.user).exclude(responseC=request.user).exclude(responseD=request.user)
    n=len(questionSet)
    if n==0:
        return None
    index=randint(0,n-1)
    ques=questionSet[index]
    tNo=contestobj.noOfQues
    quesDetail={
        'contestId':contestobj.id,
        'quesId':ques.id,
        'ques':ques.question,
        'A':ques.optionA,
        'B':ques.optionB,
        'C':ques.optionC,
        'D':ques.optionD,
        'tNo':tNo,
        'quesNo':tNo-n+1
    }
    return quesDetail


def contestCreatedDetails(request):
    user=request.user
    querySet=Contests.objects.filter(Author=user)
    contestArray=[]
    for i in querySet:
        noOfPart=len(i.participants.all())
        td={
            "contest":i.contest,
            "noOfParticipants":noOfPart,
            "startDate":i.startDate,
            "startTime":i.startTime,
            "endDate":i.endDate,
            "endTime":i.endTime,

        }

        contestArray.append(td)

    return contestArray



def contestTakenDetails(request):
    user=request.user
    querySet=Contests.objects.filter(participants=user)
    contestArray=[]
    for i in querySet:
        score=getScore(user,i)
        td={
            "contest":i.contest,
            "score":str(score)+"/"+str(i.noOfQues),
            "startDate":i.startDate,
            "startTime":i.startTime,
            "endDate":i.endDate,
            "endTime":i.endTime,
            }

        contestArray.append(td)

    return contestArray


def getScore(user,contest):
    queryset=Questions.objects.filter(contest=contest)
    score=0
    for i in queryset:
        if i.answer=='A':
            if user in i.responseA.all():
                score+=1
        if i.answer=='B':
            if user in i.responseB.all():
                score+=1   
        if i.answer=='C':
            if user in i.responseC.all():
                score+=1 
        if i.answer=='D':
            if user in i.responseD.all():
                score+=1    
    return score                     
def getUser(request):
    auth=False
    if request.user.is_authenticated:
        auth=True
    return {'a':auth,'username':request.user.username,'info':""}