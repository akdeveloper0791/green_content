# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect

from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from cmsapp.models import User,User_unique_id,My_GC_Groups,Group_users_list
import datetime
from django.http import HttpResponseRedirect
def signin(request):
    if request.method =='POST':
        user=authenticate(request,username=request.POST['email'],password=request.POST['pass'])
        if user is not None :
            login(request,user)
            messages.success(request,'you are logged in successfully')

            if request.POST.get('next') != '':
                return HttpResponseRedirect(request.POST.get('next'))

            #return HttpResponse("ok")
            else:
                return redirect('/home/')

        else:
            return render(request,'signin.html',{'error':"Please enter correct credentials"})

    else:
        if(request.user.is_authenticated):
            return redirect('/home/')
        else:
            return render(request,'signin.html')
import uuid

def signup(request):
    if request.method =='POST':
        #form= SignupForm(request.POST)
        #if form.is_valid():
        if request.POST['pass'] == request.POST['confirm_pass']:


            check_email=User.objects.filter(email=request.POST['email'])
            if len(check_email)==0:
                data={
                    'first_name':request.POST['fname'],
                    'last_name':request.POST['lname'],
                    'email':request.POST['email'],
                    'password':make_password(request.POST['pass']),
                    'username':request.POST['email']
                    }
                user=User.objects.create(**data)

                login(request,user)


                unique_key = {
                    'user_id':request.user.id,
                    'user_unique_key':uuid.uuid4().hex ,
                    }
                User_unique_id.objects.create(**unique_key)

                new_group = {
                'group_created_by':request.user,

                'group_name':request.POST['email'],
                'group_created_date' : datetime.datetime.now(),

                }

                y = My_GC_Groups.objects.create(**new_group)

                email = "{}".format(request.POST['email'])

                users_list = {
                    'group_id':y.id,
                    'group_emails_list':[str(email)],
                    'saved_emails_date':datetime.datetime.now(),

                }

                Group_users_list.objects.create(**users_list)


                messages.success(request, 'you are regesterd successfully')
                if request.POST.get('next') != '':
                    return HttpResponseRedirect(request.POST.get('next'))

            #return HttpResponse("ok")
                else:
                    return redirect('/mycontent/')


            else:
                messages.error(request, 'This email is already Exist')

                return render(request, 'signup.html',{"error":'This email is already Exist'})
        else:
            messages.error(request, 'password must be same')

            return render(request, 'signup.html',{"error":'password must be same'})


    else:


        return render(request,'signup.html')

