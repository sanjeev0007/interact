from django.shortcuts import render,redirect
from meetup.models import Register_user
from meetup.forms import RegisterForm,LoginForm,UpdateForm
from django.http import HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.core.files.storage import FileSystemStorage
import datetime
from hashing import *

def index(request):
    return render(request,'home.html')

def Register(request):
    if request.method=='POST':
       form =RegisterForm(request.POST)
       print("post")

       if form.is_valid():
           user=form.cleaned_data['first_name']
           print(user)
           us=Register_user()
           #url=confirm/user
           print("form valid")
           us.first_name=form.cleaned_data['first_name']
           name=form.cleaned_data['first_name']
           us.last_name=form.cleaned_data['last_name']
           us.email=form.cleaned_data['email']
           us.branch=form.cleaned_data['choice']
           us.curr_year=form.cleaned_data['curr_year']
           us.roll_no=form.cleaned_data['adm_no']
           user=form.cleaned_data['password']
           us.password=hash_password(user)
           print(us.password)
           us.save()
           print("branch,curr_year",us.branch,us.curr_year)

           return HttpResponseRedirect(reverse('confirm_regis',args=(name,)))

    else:
        #proposed_date=datetime.date.today()+datetime.timedelta(weeks=3)

        form=RegisterForm()
    context={
    'form':form,
    }


    return render(request,'Register.html',context)

def confirm(request,user):
    context={
    'user':user,
    }
    return render(request,'confirm_regis.html',context)

def login(request):
   if request.session.get('name'):
       nm=request.session.get('name')
       return HttpResponseRedirect(reverse('user-dashboard',args=(nm,)))
   else:

        if request.method=='POST':
            form =LoginForm(request.POST)
            print("post")

            if form.is_valid():
                 print("form valid")
                 user=form.cleaned_data['adm_no']
                 request.session['name']=user
                 print("sesssion set!")
                 return HttpResponseRedirect(reverse('user-dashboard',args=(user,)))

        else:
             print('here')
             form=LoginForm()
        context={
         'form':form,
         }

        return render(request,'login.html',context)


def dashboard(request,user):
    if request.session.get('name'):
        us=Register_user.objects.get(roll_no=user)
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            us.img_link=uploaded_file_url
            us.save()
            print(uploaded_file_url)
            return render(request, 'dashboard.html', {
                'us':us,'user':user,
            })
        return render(request,'dashboard.html',{'user':user,'us':us})

    else:
        return login(request)

def logout(request):
    try:
          del request.session['name']
          print("user deleted")
    except :
          pass
    return HttpResponseRedirect(reverse('login_user'))

def profile(request,user):
    us=Register_user.objects.get(roll_no=user)

    if request.method=='POST':
       form =UpdateForm(request.POST,request.FILES)
       print("post")

       if form.is_valid():
           print("form valid")
           us.github=form.cleaned_data['github_link']
           us.email=form.cleaned_data['email']
           us.save()
           return HttpResponseRedirect(reverse('user-dashboard',args=(user,)))

    else:
        #proposed_date=datetime.date.today()+datetime.timedelta(weeks=3)
       print(us.first_name)
       form=UpdateForm(initial={'email':us.email,'github_link':us.github})
    context={
    'name':us.first_name,
    'branch':us.branch,
    'form':form,
    }
    return render(request,'profile.html',context=context)






'''def confirm(request,user):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        print(filename)
        return render(request, 'confirm_regis.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'confirm_regis.html')
'''
