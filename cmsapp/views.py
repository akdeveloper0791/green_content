

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import re
#import user

import os

import bs4 as bs4
import requests

#import json
#import selenium
#from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
#from django.core import mail
#from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, redirect,get_object_or_404
#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#from cmsapp.forms import LoginForm
from django.contrib.auth import login, authenticate
from cmsapp.models import Youtube_links,Images_links,News_links,Searched_videos,Access_Token,Searched_images,Upload,My_GC_Groups,Group_users_list,Upload,Keywords,Rest,Single_campaign_upload,Multiple_campaign_upload,Multiple_campaign_files,User_unique_id
from django.db.models import Q
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from player.models import Last_Seen_Metrics;
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template

@login_required
def home(request):
    return JsonResponse({'home':'sweet home'})
    #if request.user.is_authenticated:
        #return redirect("/campaigns/list_camp_web/")
    

def web_search(request):
    return render(request,'webcontent.html')

def signageserv(request):
    server = request.META['SERVER_NAME'];
    if server == 'ADSKITE':
        return render(request,'ihealthtv.html')
    else:
       return render(request,'signageserv.html')

def all_content(request):
    if request.user.is_authenticated():
        if request.method == 'GET':
            # ----------- video links code -------------
            video_page=[]
            video_Link = []
            videos_data =[]
            l=[]
            key = request.GET['keyword']
            url="https://www.youtube.com/results?search_query="+str(key)

            response = requests.get(url)
            html = response.content
            soup = bs4.BeautifulSoup(html , 'html.parser')

            for vid in soup.findAll('a',{'class':'yt-uix-button vve-check yt-uix-sessionlink yt-uix-button-default yt-uix-button-size-default'}):

                video_page.append(vid.get('href'))

            for i in video_page:
                i=str(i)
                p=i[i.find('?')+1:i.find('&')]
                video_Link.append("https://www.youtube.com/results?search_query="+str(key)+"&"+p)

            for i in video_Link:

                response = requests.get(i)
                html = response.content # attrs={'class':'yt-uix-tile-link'}
                soup = bs4.BeautifulSoup(html,'html.parser')
                for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):

                    res = 'https://www.youtube.com' + vid['href']
                    lid=vid['href']
                    titles=vid['title'].split('|')[0]
                    req=[]+[res,titles,key,lid]
                    l.append(req)

            for i in range(len(l)):

                results= re.sub(r"(?ism).*?=(.*?)$", r"https://www.youtube.com/embed/\1",l[i][0])

                result=[]+[results,l[i][1],l[i][2],l[i][3],'videos']
                videos_data.append(result)

            # --------- images crawl code ----------

            key=key.replace(" ", "")

            l=[]
            images_data =[]

            url="https://www.bing.com/images/search?q="+key+"&qs=n&form=QBIR"

            response = requests.get(url)
            r_data=response.content
            soup = bs4.BeautifulSoup(r_data , 'html.parser')

            for vid in soup.findAll('a',{'class':'thumb'}):

                l.append(vid.get('href'))
            for res in l:

                i=str(res)

                ids= i.split("/",1)[-1]
                image=[]+[i,key,ids]
                images_data.append(image)


            key=key.replace(" ", "")


            news_data = []

            url="https://www.google.com/search?q="+key+"&tbm=nws&source=lnms&sa=X&ved=0ahUKEwiBkeL33__bAhWINI8KHbuWDqcQ_AUICygC&biw=1366&bih=655&dpr=1"
            url1="https://www.google.co.in/search?q="+key+"&biw=1366&bih=655&tbm=nws&ei=TXg8W7LeBMTbvASgjqyABA&start=10&sa=N"
            n=[url,url1]


            for i in n:
                response = requests.get(url)
                html = response.content
                soup = bs4.BeautifulSoup(html , 'html.parser')

                for res in soup.find_all('div',{'class':'g'}):

                    link=res.find('a').get('href')
                    link=str(link)
                    word=link.find('q=')
                    word1=link.find('&sa')
                    final_link=link[word+2:word1]

                    Uid=link[word1:]
                    content=(res.find('div',{'class':'st'}).text).encode('utf-8')

                    img_url=res.find('img')
                    if img_url is None:
                        pass
                    else:
                        z=[]+[final_link,res.find('a').text,Uid,img_url.get('src'),content,key]
                        news_data.append(z)

            #data = {'videos':videos_data ,'images': images_data, 'news': news_data }
            return render(request,'result.html')
    else:
        return redirect('/signagecms/signin/')






# ---------   previous search code with all images,videos,news ,marketing   -------------

o=[]
@login_required
def search(request):

    if request.method == 'GET':
        #x = request.GET['keyword']
        if 'youtube' in request.GET :
            key = request.GET['keyword']
            del o[:]
            db_search_data = Searched_videos.objects.filter(keyword=key.lower()).order_by('id')[:20]
            if db_search_data:
                for i in db_search_data:
                    result = []+[i.videos_link,i.title,i.keyword,i.video_id,i.id]
                    o.append(result)

                check_links =[]
                db_saveddata=[]
                x= Youtube_links.objects.filter(user=request.user.id,keyword=key.lower())
                if x:
                    for i in x:
                        check_links = check_links+[i.video_link]
                        y = []+[i.video_link,i.title,i.keyword,i.id,i.vid_id]
                        db_saveddata.append(y)
                return render(request,'result.html',{'videos_new':o,'videos_old':db_saveddata,'key':key})


            else:
                page=[]
                finalLink=[]
                l=[]
                forlink=[]

                url="https://www.youtube.com/results?search_query="+str(key.lower())
                response = requests.get(url)
                html = response.content
                soup = bs4.BeautifulSoup(html , 'html.parser')

                for vid in soup.findAll('a',{'class':'yt-uix-button vve-check yt-uix-sessionlink yt-uix-button-default yt-uix-button-size-default'}):

                    page.append(vid.get('href'))


                for i in page:
                    i=str(i)
                    p=i[i.find('?')+1:i.find('&')]
                    finalLink.append("https://www.youtube.com/results?search_query="+str(key.lower())+"&"+p)

                for i in finalLink:

                    response = requests.get(i)
                    html = response.content # attrs={'class':'yt-uix-tile-link'}
                    soup = bs4.BeautifulSoup(html,'html.parser')
                    for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):

                        res = 'https://www.youtube.com' + vid['href']
                        lid=vid['href']
                        titles=vid['title'].split('|')[0]
                        req=[]+[res,titles,key,lid]
                        l.append(req)

                for i in range(len(l)):

                    video_link= re.sub(r"(?ism).*?=(.*?)$", r"https://www.youtube.com/embed/\1",l[i][0])
                    if video_link in forlink:
                        pass
                    else:

                        #result=[]+[video_link,l[i][1],l[i][2],l[i][3],'videos']
                        #o.append(result)
                        db = Searched_videos()
                        db.keyword = key
                        db.title = l[i][1]
                        db.videos_link = video_link
                        db.video_id = l[i][3]
                        db.created_date = datetime.datetime.now()

                        db.save()
                del o[:]
                x= Searched_videos.objects.filter(keyword=key.lower()).order_by('id')[:20]
                        #check_links = []
                if x:
                    for i in x:
                                #check_links = check_links+[i.video_link]
                        result = []+[i.videos_link,i.title,i.keyword,i.video_id,i.id]
                        o.append(result)
                return render(request,'result.html',{'videos_new':o,'key':key})

                #db_saveddata=[]
                '''page = request.GET.get('page', 1)

                paginator = Paginator(o, 18)
                try:
                    new=paginator.page(page)
                except PageNotAnInteger:
                    new=paginator.page(1)
                except EmptyPage:
                    new=paginator.page(paginator.num_pages)
                return render(request,'result.html',{'videos_new':new,'key':key})'''

        elif 'images' in request.GET:

            key = request.GET['keyword']

            key=key.replace(" ", "")
            del o[:]

            db_search_data = Searched_images.objects.filter(keyword=key.lower())
            if db_search_data:
                for i in db_search_data:
                    result = []+[i.images_link,i.keyword,i.id]
                    o.append(result)

                db_data = []

                check_links =[]

                x = Images_links.objects.filter(user=request.user.id,keyword=key.lower())

                if x:
                    for i in x:
                        check_links.append(i.image_link)
                        link=[]+[i.image_link,i.keyword,i.id]
                        db_data.append(link)

                return render(request,'result.html',{'images_new':o,'images_old':db_data,'key':key})

            else:
                l=[]

                url="https://www.bing.com/images/search?q="+key.lower()+"&qs=n&form=QBIR"

                response = requests.get(url)
                r_data=response.content
                soup = bs4.BeautifulSoup(r_data , 'html.parser')

                for vid in soup.findAll('a',{'class':'thumb'}):

                    l.append(vid.get('href'))
                for res in l:

                    link =str(res)

                    ids= link.split("/",1)[-1]
                    #image=[]+[i,key,ids]
                    db = Searched_images()
                    db.keyword = key
                    db.title = ids
                    db.images_link = link
                    db.image_id = ids
                    db.created_date = datetime.datetime.now()

                    db.save()
                del o[:]

                x= Searched_images.objects.filter(keyword=key.lower())

                if x:
                    for i in x:
                        result = []+[i.images_link,i.keyword,i.id]
                        o.append(result)

                return render(request,'result.html',{'images_new':o,'key':key})

            '''page = request.GET.get('page', 1)

            paginator = Paginator(o, 12)
            try:
                new=paginator.page(page)
            except PageNotAnInteger:
                new=paginator.page(1)
            except EmptyPage:
                new=paginator.page(paginator.num_pages)'''

        elif 'news' in request.GET :
            key = request.GET['keyword']

            key=key.replace(" ", "")

            check_links=[]
            db_data=[]

            x = News_links.objects.filter(user=request.user.id,keyword=key.lower())

            if x:
                for i in x:
                    check_links.append(i.news_link)
                    link=[]+[i.news_link,i.title,i.content,i.image,i.id]
                    db_data.append(link)

            url="https://www.google.com/search?q="+key.lower()+"&tbm=nws&source=lnms&sa=X&ved=0ahUKEwiBkeL33__bAhWINI8KHbuWDqcQ_AUICygC&biw=1366&bih=655&dpr=1"
            url1="https://www.google.co.in/search?q="+key.lower()+"&biw=1366&bih=655&tbm=nws&ei=TXg8W7LeBMTbvASgjqyABA&start=10&sa=N"
            n=[url,url1]

            del o[:]
            for i in n:
                response = requests.get(url)
                html = response.content
                soup = bs4.BeautifulSoup(html ,'html.parser')

                for res in soup.find_all('div',{'class':'g'}):

                    link=res.find('a').get('href')
                    link=str(link)
                    word=link.find('q=')
                    word1=link.find('&sa')
                    final_link=link[word+2:word1]
                    if final_link in check_links:
                        pass
                    else:

                        Uid=link[word1:]
                        content=(res.find('div',{'class':'st'}).text).encode('utf-8')

                        img_url=res.find('img')
                        if img_url is None:
                            pass
                        else:
                            z=[]+[final_link,res.find('a').text,Uid,img_url.get('src'),content,key]
                            o.append(z)


            return render(request,'result.html',{'news_new':o,'new_old':db_data,'key':key})
            #return HttpResponse(o)

        elif 'marketing' in request.GET :
            return HttpResponse('marketing')
        else:
            pass
            '''page = request.GET.get('page', 1)

            paginator = Paginator(o, 12)
            try:
                new=paginator.page(page)
            except PageNotAnInteger:
                new=paginator.page(1)
            except EmptyPage:
                new=paginator.page(paginator.num_pages)
            return render(request,'result.html',{'videos_new':new})'''



def login_auth():
    token_url = 'http://159.89.172.189/api/authorize/access_token'
    login_url = 'http://159.89.172.189/api/user'
    client_id  = 'DPVW8hUHlFMullOM4YVmurdBKfVZKZHtshqEuqlk'
    client_secret  = 'hKblJgU7OWoqKfuZ34lJRCoTk7OWqmaBNmiKIHfCbiKPa31kaJcNxnpAIxH0NrhiHkcHYJpRT8orR3MhzMWFRxl1bUycas5S5MEo4GeowlUIifZ3ofC01omDPaYwII9NlbNwLgxzaIszHxUt5DKrSuV1dCldFPUEdzqwb9Gg0gtkDGAkn4UoIde5rzRzOnif6jImpttO9A3kblRIskyhYHEteQdcn7SkwJ2eXJZiXyUJsaK4WHJVfkLWU32R4K'

    data = {'grant_type':'client_credentials'}

    access_response = requests.post(token_url,data=data,verify=False,allow_redirects=False,auth=(client_id, client_secret))

    y = access_response.json()
    headers = {'Authorization': "Bearer " +y["access_token"],'Cache-Control':'no-cache'}

    response = requests.get(login_url, headers=headers)
    result = response.json()
    #return HttpResponse(result)
    #usernames = []
    #del usernames[:]
    for i in result:
        #usernames.append(str(i["userName"]))
        x = User.objects.filter(username=str(i["userName"]))
        if x:
            pass
        else:
            data = {"username":i["userName"],'password':make_password("adskite123")}
            User.objects.create(**data)

    return result


import os
from pytube import YouTube

import random
@login_required
def video_upload(request):

    link= request.GET['link']
    title= request.GET['title']
    basename = str(title)
    basename = basename.replace(' ','_')
    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    filename = "_".join([basename, suffix])

    video_upload_download(link,filename)
    filename = str(filename)+'.mp4'

    token_url = "http://159.89.172.189/api/authorize/access_token"
    library = 'http://159.89.172.189/api/library'
    check_db = Access_Token.objects.filter(ss_username=request.user.username)
    if check_db:
        for i in check_db:
            client_id  = i.ss_client_id
            client_secret  = i.ss_client_secret

            data = {'grant_type':'client_credentials'}

            access_response = requests.post(token_url,data=data,verify=False,allow_redirects=False,auth=(client_id, client_secret))

            y = access_response.json()
            headers = {'Authorization': "Bearer " +y["access_token"],'Cache-Control':'no-cache'}
            THIS_FOLDER =os.path.dirname(__file__)
            my_file = os.path.join(THIS_FOLDER,filename)

            video_file = {'files':open(my_file,'rb')}
            mediaId_response=requests.post(library, headers=headers ,files = video_file)

            os.remove(my_file)

            return HttpResponse(mediaId_response.text)
@login_required
def images_upload(request):

    link= request.GET['link']

    image=image_upload_download(link)

    check_db = Access_Token.objects.filter(ss_username=request.user.username)
    if check_db:
        for i in check_db:
            client_id = i.ss_client_id
            client_secret = i.ss_client_secret
            token_url = "http://159.89.172.189/api/authorize/access_token"

            library = 'http://159.89.172.189/api/library'

            data = {'grant_type':'client_credentials'}

            response = requests.post(token_url,data=data,verify=False,allow_redirects=False,auth=(client_id,client_secret))
            y = response.json()
            headers = {'Authorization': "Bearer " +y["access_token"],'Cache-Control':'no-cache'}
            THIS_FOLDER =os.path.dirname(__file__)
            my_file = os.path.join(THIS_FOLDER,image)

            image_file = {'files':open(my_file,'rb')}
            mediaId_response=requests.post(library, headers=headers ,files = image_file)
            os.remove(my_file)

            return HttpResponse(mediaId_response.text)

    #os.remove(my_file)

@login_required
def video_upload_download(link,filename):

    yt = YouTube(link)



    yt.streams.first().download("/home/adskite/myproject/signagecms/cmsapp",filename=str(filename))


    return
@login_required
def image_upload_download(link):

    name=link.split('/')[-1]
    img_data = requests.get(link).content
    with open('/home/adskite/myproject/signagecms/cmsapp/'+str(name), 'wb') as handler:
        handler.write(img_data)

    return name
@login_required
def downloads_videos(request,num):
    check = Searched_videos.objects.filter(id=int(num))
    if check:
        link = check[0].videos_link
        name =  check[0].keyword
        #return HttpResponse(link)
    #link = request.GET['link']
    #if request.method == "GET":
        fname = downloads_video_local(link,name)
        if fname == "error":
            return render(request,"dl_error.html",{"link":link})


        filename = str(fname)+'.mp4'

        with open("/home/adskite/myproject/signagecms/static/downloads/videos/{}".format(filename),'rb') as fh:
            response = HttpResponse(fh, content_type="application/vnd.android.package-archive")
            response["Content-disposition"] = "attachment; filename={}".format(filename)
        x = response
        THIS_FOLDER =os.path.dirname("/home/adskite/myproject/signagecms/static/downloads/videos/")
        my_file = os.path.join(THIS_FOLDER,filename)
        os.remove(my_file)
        return x
@login_required
def downloads_images(request,num):
    check = Searched_images.objects.filter(id=int(num))
    if check:
        link = check[0].images_link

    #if request.method == "GET":
        #link = request.GET['link']
        filename = downloads_image_local(link)
        #filename = filename+'.jpg'
        #filename = filename
        #response = JsonResponse({'status':True, 'result':filename})
        #return response



        with open("/home/adskite/myproject/signagecms/static/downloads/images/{}".format(filename),'rb') as fh:
            response = HttpResponse(fh, content_type="application/vnd.android.package-archive")
            response["Content-disposition"] = "attachment; filename={}".format(filename)

        x = response
        THIS_FOLDER =os.path.dirname("/home/adskite/myproject/signagecms/static/downloads/images/")
        my_file = os.path.join(THIS_FOLDER,filename)
        os.remove(my_file)
        return x



def downloads_image_local(link):

    ran = random.randint(0,100000000)
    name = str(ran)+'.jpg'
    img_data = requests.get(link).content
    with open('/home/adskite/myproject/signagecms/static/downloads/images/'+str(name), 'wb') as handler:
        handler.write(img_data)

    return name

from pytube import YouTube

def downloads_video_local(link,name):
    try:
        yt = YouTube(link)
        basename = str(name)
        basename = basename.replace(' ','_')
        suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        filename = "_".join([basename, suffix])
    #ran = random.randint(0,100000000)
    #filename = str(ran)
        stream = yt.streams.filter(only_video = True, file_extension = "mp4")
        stream.first().download("/home/adskite/myproject/signagecms/static/downloads/videos",filename=filename)
        return filename
    except:
        filename = "error"
        return filename

def testing(request):
    return render(request,"signup.html")

@api_view(['GET'])
@login_required
def youtube_content(request):
    if request.method == "GET":

        if request.user.is_authenticated():

            data = {
                'video_link':request.GET['link'],
                'title': request.GET['title'],
                'keyword' : request.GET['keyword'],
                'created_date' : datetime.datetime.now(),
                'user' : request.user.id,
                'vid_id' : request.GET['video_id']


            }
            Youtube_links.objects.create(**data)

            return HttpResponse("ok")

        else:
            return render(request, 'login.html')

def images_content(request):
    if request.method == "GET":

       data = {
           'image_link':request.GET['link'],
           'title': request.GET['title'],
           'keyword' : request.GET['keyword'],
           'created_date' : datetime.datetime.now(),
           'user' : request.user.id

       }
       Images_links.objects.create(**data)
       return HttpResponse("ok")

@api_view(['GET'])
def news_content(request):
    if request.method == "GET":

       data = {
           'image':request.GET['image'],
           'title':request.GET['title'],
           'news_links':request.GET['link'],
           'content': request.GET['content'],
           'keyword' : request.GET['keyword'],
           'created_date' : datetime.datetime.now(),
           'user' : request.user.id


       }
       News_links.objects.create(**data)
       return HttpResponse("ok")


def my_wishlist(request):

    return render(request,'dashboard.html')

def my_videos(request):
    x = Youtube_links.objects.filter(user=request.user.id)
    o=[]
    if x:
        for i in x:
            l=[]+[i.video_link,i.title,i.keyword,i.id]
            o.append(l)
        x = JsonResponse({'status': True, 'result': o})
        return x
    else:
        x = JsonResponse({'status': False, 'result': "Currently, you don't have videos in your whishlist"})
        return x


def my_images(request):
    x = Images_links.objects.filter(user=request.user.id)
    o=[]
    if x:
        for i in x:
            l=[]+[i.image_link,i.title,i.keyword,i.id]
            o.append(l)
        x = JsonResponse({'status': True, 'result': o})
        return x
    else:
        x = JsonResponse({'status': False, 'result': "currently, you don't have Images in your whishlist"})
        return x


def my_news(request):
    x= News_links.objects.filter(user=request.user.id)
    o=[]
    if x:
        for i in x:
            l=[]+[i.image,i.news_link,i.content,i.keyword,i.id]
            o.append(l)

        x = JsonResponse({'status': True, 'result': o})
        return x

    else:
        x = JsonResponse({'status': False, 'result': "currently, you don't have News in your whishlist"})
        return x

def videos_remove(request,pk):
    x=Youtube_links.objects.get(id=pk)
    x.delete()
    video_name = x.title
    if x:
        y = JsonResponse({'status': True, 'result': "'%s' has been deleted successfully" %(video_name)})
        return y
    else:
        y = JsonResponse({'status': True, 'result': "unable to delete this video"})
        return y

def images_remove(request,pk):
    x=Images_links.objects.get(id=pk)
    x.delete()
    image_name = x.title
    if x:
        y = JsonResponse({'status': True, 'result': "'%s' has been deleted successfully" %(image_name)})
        return y
    else:
        y = JsonResponse({'status': True, 'result': "unable to delete this image"})
        return y
def news_remove(request,pk):
    News_links.objects.get(id=pk).delete()
    return redirect('/signagecms/my_wishlist/')



def signout(request):
    logout(request)
    return redirect('/signageserv/')


def about_us(request):
    return render(request,'about.html')

def terms_services(request):
    return render(request,'terms.html')

def privacy_services(request):
    return render(request,'privacy.html')


def contact_us(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        subject = 'Contact Form'
        from_email = settings.EMAIL_HOST_USER
        to_email = [settings.EMAIL_HOST_USER]

        context = {
         'user' :name,
         'email' : email,
         'message' : message,
        }

        contact_message = get_template('contact_message.txt').render(context)
        
        send_mail(subject,contact_message,from_email,to_email,fail_silently= True)

        return render(request,'contact.html',{"success":"Message sent successfully, our team will reply shortly "})
      
    else:
        return render(request,'contact.html')

from django.conf import settings
from django.core.files.storage import FileSystemStorage
@login_required
def campaign_upload(request):
    if request.method == "POST":

        media_file = request.FILES.getlist('media_file')
        if media_file:
            for i in media_file:
                n= i.name
                s = n.split('.')[-1]
                if s == "txt":
                    camp_name = n.split('.')[0]
                    t_file = i
            cam_check = Multiple_campaign_upload.objects.filter(campaign_uploaded_by=request.user.id,campaign_name = camp_name)
            if len(cam_check)== 0:
                unique_key = User_unique_id.objects.get(user_id = request.user.id)
                #static_media_path = '/home/adskite/myproject/signagecms/media/campaigns/{}/'.format(camp_name)
                folder='/home/adskite/myproject/signagecms/media/campaigns/{}/{}/'.format(unique_key.user_unique_key,camp_name)
                fs = FileSystemStorage(location=folder) #defaults to   MEDIA_ROOT
                #filename = fs.save(myfile.name, myfile)
                d = Multiple_campaign_upload()
                d.campaign_uploaded_by = request.user.id
                d.campaign_name = camp_name
                file_n = fs.save(t_file.name, t_file)
                d.text_file = '/campaigns/{}/{}/{}'.format(unique_key.user_unique_key,camp_name,t_file.name)
                d.created_date = datetime.datetime.now()
                d.updated_date = datetime.datetime.now()
                d.save()

                for i in media_file:
                    n= i.name
                    s = n.split('.')[-1]
                    if not s == "txt":

                        f = Multiple_campaign_files()
                        f.Multiple_campaign = d.id
                        med_sile_n = fs.save(i.name, i)
                        f.mul_files = '/campaigns/{}/{}/{}'.format(unique_key.user_unique_key,camp_name,i.name)
                        f.save()
                return render(request,'campaign_upload.html',{'res':"Campaign upload successful"})
            else:
                return render(request,'campaign_upload.html',{'res':"Campaign Name already exist"})


        else:

            x = JsonResponse({'status': False, 'result': "media files should not be empty" })
            return x

    else:
        #return HttpResponse("ok")
        return render(request,'campaign_upload.html')
@login_required
def single_campaign_preview(request):
    x= Single_campaign_upload.objects.filter(campaign_uploaded_by = request.user.id)
    return render(request,'single_campaigns.html',{'res':x})

@login_required
def api_videos(request):
    x= Searched_videos.objects.filter(keyword='biryani')
    res = []
    for i in x:
        result = []+[i.videos_link,i.title,i.keyword,i.video_id,i.id]
        res.append(result)

    x = JsonResponse({'status': True, 'result': res})
    return x
@login_required
def api_images(request):
    x= Searched_images.objects.filter(keyword='biryani')
    res = []
    for i in x:
        result = []+[i.images_link,i.keyword,i.id]
        res.append(result)

    x = JsonResponse({'status': True, 'result': res})
    return x

from django.utils import timezone

@login_required
def upload(request):

    if request.method == 'POST':

        file = request.FILES['file']
        desc = request.POST['desc']
        keys = request.POST['keys']
        #y=keys.decode('utf-8').split(',')
        y=keys.split(',')
        type=  request.POST['Private']
        group = request.POST['email_gc_name']
        if len(group) == 1:
            groupid = []+[group]
        elif group[0]=="multiselect-all":
            groupid = group[1:]
        else:
            groupid = group
        #return HttpResponse(group_id)
        video_types = ['wmv','avi','mpeg','mpg','3gp','webm','mp4','mkv']

        image_types = ['jpg','jpeg','png','bmp','gif']

        audio_types = ['mp3','m4a','ts','flac','wav','ogg','xmf','ota']
        #return HttpResponse(request.POST['groups'])
        file_name = str(file.name).split('.')[-1]
        if str(file_name) in video_types:
            db1 = Upload()
            db1.upload = file
            db1.desc = desc
            db1.file_access_mode = type
            db1.file_type = "video"
            db1.user = request.user
            db1.group_id = groupid
            db1.created_date  = timezone.now()

            db1.save()

            subject = 'Gc info'
            message = 'https://www.greencontent.in/change_password/'
            from_email = settings.EMAIL_HOST_USER
            to_list= []
            for i in groupid:
                email_check = Group_users_list.objects.get(group_id = str(i))
                #to_list.append(i)
                to_list= email_check.group_emails_list
                #to_list.append(email_check.email)
                send_mail(subject, message, from_email,to_list,fail_silently=True)

            #db1 = {"upload": file, "desc": desc, "file_access_mode": type,"file_type":"video","user":request.user,"group_id":request.POST['groups'] if 'groups' in request.POST['groups']}
            #x = Upload.objects.create(**db1)
            #x.save()
            for i in y:
                db2 = Keywords()
                db2.keys = str(i)
                db2.upload_id = db1.id
                db2.save()
            '''y = os.listdir(os.path.join(settings.MEDIA_ROOT))
            for i in y:
                os.remove(os.path.join(settings.MEDIA_ROOT, str(i)))'''

            return redirect("/mycontent_videos/")
        elif str(file_name) in image_types:
            db1 = Upload()
            db1.upload = file
            db1.desc = desc
            db1.file_access_mode = type
            db1.file_type = "image"
            db1.user = request.user

            db1.group_id = groupid
            db1.created_date  = timezone.now()

            db1.save()

            subject = 'Gc info'
            message = 'https://www.greencontent.in/change_password/'
            from_email = settings.EMAIL_HOST_USER
            group_emails_list= []
            #return HttpResponse(groupid)

            email_check = Group_users_list.objects.filter(group_id__in=groupid)
            return HttpResponse(email_check)
            for j in email_check:

                group_emails_list.append(i)
            return HttpResponse(group_emails_list)
            for k in  group_emails_list:

                to_list= k
                #to_list.append(email_check.email)
                send_mail(subject, message, from_email,to_list,fail_silently=True)

            #db = {"upload": file, "desc": desc, "file_access_mode": type, "file_type": "image","user":request.user,"group_id":request.POST['groups'] if 'groups' in request.POST['groups']}
            #x = Upload.objects.create(**db)
            #x.save()

            for i in y:
                db2 = Keywords()
                db2.keys = str(i)
                db2.upload_id= db1.id
                db2.save()
            '''y = os.listdir(os.path.join(settings.MEDIA_ROOT))
            for i in y:
                os.remove(os.path.join(settings.MEDIA_ROOT, str(i)))'''

            return redirect("/mycontent_images/")
        elif str(file_name) in audio_types:
            db1 = Upload()
            db1.upload = file
            db1.desc = desc
            db1.file_access_mode = type
            db1.file_type = "video"
            db1.user = request.user
            db1.group_id = groupid
            db1.created_date  = timezone.now()

            db1.save()

            subject = 'Gc info'
            message = 'https://www.greencontent.in/change_password/'
            from_email = settings.EMAIL_HOST_USER
            to_list= []
            for i in group_id:
                email_check = User.objects.get(id = i)

                to_list.append(email_check.email)
            send_mail(subject, message, from_email,to_list,fail_silently=True)

            for i in y:
                db2 = Keywords()
                db2.keys = str(i)
                db2.upload_id = db1.id
                db2.save()
            '''y = os.listdir(os.path.join(settings.MEDIA_ROOT))
            for i in y:
                os.remove(os.path.join(settings.MEDIA_ROOT, str(i)))'''

            return HttpResponse("success")
        else:
            #return HttpResponse("unsupported file")
              y = JsonResponse({'status': False, 'result': "unsupported file" })
              return y
    else:
        #x = Upload.objects.filter(file_type = "image")

        #for i in x:
                #l = [i.user,str(i.upload),i.keys,i.desc,i.file_access_mode]
                #res.append(i.upload)
        return render(request,'upload.html')
@login_required
def upload_api(request):

    if request.method == 'GET':

        file = request.FILES['file']
        desc = request.GET['desc']
        keys = request.GET['keys']
        y=keys.decode('utf-8').split(',')
        type=  request.GET['Private']
        group = request.GET['email_gc_name']
        if len(group) == 1:
            group_id = []+[group]
        elif group[0]=="multiselect-all":
            group_id = group[1:]
        else:
            group_id = group
        video_types = ['wmv','avi','mpeg','mpg','3gp','webm','mp4','mkv']

        image_types = ['jpg','jpeg','png','bmp','gif']

        audio_types = ['mp3','m4a','ts','flac','wav','ogg','xmf','ota']
        #return HttpResponse(request.POST['groups'])
        file_name = str(file.name).split('.')[-1]
        if str(file_name) in video_types:
            db1 = Upload()
            db1.upload = file
            db1.desc = desc
            db1.file_access_mode = type
            db1.file_type = "video"
            db1.user = request.user
            db1.group_id = group_id
            db1.created_date  = timezone.now()
            db1.save()

            subject = 'Gc info'
            message = 'https://www.greencontent.in/change_password/'
            from_email = settings.EMAIL_HOST_USER
            to_list= []
            for i in group_id:
                email_check = User.objects.get(id = str(i))

                to_list.append(email_check.email)
            send_mail(subject, message, from_email,to_list,fail_silently=True)


            #db1 = {"upload": file, "desc": desc, "file_access_mode": type,"file_type":"video","user":request.user,"group_id":request.POST['groups'] if 'groups' in request.POST['groups']}
            #x = Upload.objects.create(**db1)
            #x.save()
            for i in y:
                db2 = Keywords()
                db2.keys = str(i)
                db2.upload_id = db1.id
                db2.save()
            '''y = os.listdir(os.path.join(settings.MEDIA_ROOT))
            for i in y:
                os.remove(os.path.join(settings.MEDIA_ROOT, str(i)))'''
            res = JsonResponse({'status': True, 'result': "submitted successfully"})
            return res
            #return redirect("/mycontent_videos/")
        elif str(file_name) in image_types:
            db1 = Upload()
            db1.upload = file
            db1.desc = desc
            db1.file_access_mode = type
            db1.file_type = "image"
            db1.user = request.user

            db1.group_id = group_id
            db1.created_date  = timezone.now()

            db1.save()

            subject = 'Gc info'
            message = 'https://www.greencontent.in/change_password/'
            from_email = settings.EMAIL_HOST_USER
            to_list= []
            if group_id.startswith('['):
                line = group_id.strip('[]\n')
                list_of_strs = line.split(',')

                z=[i for i in list_of_strs]
            for i in z:

                email_check = User.objects.get(id = i)

                #to_list.append(email_check.email)
                to_list.append(email_check)
            return HttpResponse(to_list)
            send_mail(subject, message, from_email,to_list,fail_silently=True)

            #db = {"upload": file, "desc": desc, "file_access_mode": type, "file_type": "image","user":request.user,"group_id":request.POST['groups'] if 'groups' in request.POST['groups']}
            #x = Upload.objects.create(**db)
            #x.save()

            for i in y:
                db2 = Keywords()
                db2.keys = str(i)
                db2.upload_id= db1.id
                db2.save()
            '''y = os.listdir(os.path.join(settings.MEDIA_ROOT))
            for i in y:
                os.remove(os.path.join(settings.MEDIA_ROOT, str(i)))'''
            res = JsonResponse({'status': True, 'result': "submitted successfully"})
            return res
            #return redirect("/mycontent_images/")
        elif str(file_name) in audio_types:
            db1 = Upload()
            db1.upload = file
            db1.desc = desc
            db1.file_access_mode = type
            db1.file_type = "audio"
            db1.user = request.user
            db1.group_id = group_id
            db1.created_date  = timezone.now()


            db1.save()

            subject = 'Gc info'
            message = 'https://www.greencontent.in/change_password/'
            from_email = settings.EMAIL_HOST_USER
            to_list= []
            for i in group_id:
                email_check = User.objects.get(id = str(i))

                to_list.append(email_check.email)
            send_mail(subject, message, from_email,to_list,fail_silently=True)

            for i in y:
                db2 = Keywords()
                db2.keys = str(i)
                db2.upload_id = db1.id
                db2.save()
            '''y = os.listdir(os.path.join(settings.MEDIA_ROOT))
            for i in y:
                os.remove(os.path.join(settings.MEDIA_ROOT, str(i)))'''
            res = JsonResponse({'status': True, 'result': "submitted successfully"})
            return res
            #return HttpResponse("success")
        else:
            res = JsonResponse({'status': False, 'result': "unsupported file"})
            return res
            #return HttpResponse("unsupported file")
    else:
        #x = Upload.objects.filter(file_type = "image")

        #for i in x:
                #l = [i.user,str(i.upload),i.keys,i.desc,i.file_access_mode]
                #res.append(i.upload)
        return render(request,'upload.html')
@api_view(['POST','GET'])
@login_required
def edit_upload_post(request,k):
    if request.method == "GET":
        y=request.GET['keys'].decode('utf-8').split(',')
        x = Upload.objects.get(id = k)
        x.desc = request.GET['desc']
        x.group_id = request.GET['email_gc_name']
        x.file_access_mode = request.GET['select_type']
        x.save()

        for i in y:
                db2 = Keywords()
                db2.keys = str(i)
                db2.upload_id = k
                db2.save()

        res = JsonResponse({'status': True, 'result': "submitted successfully"})
        return res

@login_required
def edit_upload(request,k):

    d= {}

    keys = []
    x = get_object_or_404(Upload,id = k)
    y= Keywords.objects.filter(upload_id = k)
        #z = get_object_or_404(My_GC_Groups,id = x.group_id)

    if y:
        for i in y:
            keys.append(i.keys)

    d["id"] = x.id
    d["upload_name"] = x.upload.name
    d["keywords"] = keys
    d["desc"] = x.desc
    d["file_type"] = x.file_type
    d["file_access_mode"] = x.file_access_mode
    d["group_id"] = x.group_id
    res = JsonResponse({'status': True, 'result': d})
    return res
@login_required
def mycontent_images_api(request):
    x = Upload.objects.filter(file_type = "image",user=request.user)
    #y= Upload.objects.filter(file_type = "image",file_access_mode = "public")

    if x:
        return render(request,'mycontent_images.html',{'private_result': x})


    else:

        return render(request,'mycontent_images.html',{'empty': "currently you don't have your own data ..."})


@login_required
def mycontent_videos_api(request):
    x = Upload.objects.filter(file_type = "video",user=request.user)
    #y= Upload.objects.filter(file_type = "video",file_access_mode = "public")

    if x:
        return render(request,'mycontent_videos.html',{'private_result': x})
    else:
       return render(request,'mycontent_videos.html',{'empty': "currently you don't have your own data ..."})

def mycontent_audios_api(request):
    x = Upload.objects.filter(file_type = "audio",user=request.user)
    #y= Upload.objects.filter(file_type = "video",file_access_mode = "public")

    if x:
        return render(request,'mycontent_audios.html',{'private_result': x})
    else:
       return render(request,'mycontent_audios.html',{'empty': "currently you don't have your own data ..."})


@login_required
def my_content(request):
    return render(request,'my_content.html')


def downloads_upload_files(request,pk):
    x = Upload.objects.filter(id = pk)
    filename = ''
    for i in x:
        filename = filename+str(i.upload.name)
    with open("/home/adskite/myproject/signagecms/media/{}".format(filename),'rb') as fh:
            response = HttpResponse(fh, content_type="application/vnd.android.package-archive")
            response["Content-disposition"] = "attachment; filename={}".format(filename)
            response['X-Sendfile'] = "/home/adskite/myproject/signagecms/media/{}".format(filename)

            return response

def remove_upload_files(request,pk):
    x=Upload.objects.get(id = pk)
    x.delete()
    if x:
        y = JsonResponse({'status': True, 'result': " file has been deleted successfully"})
        return y
    else:
        y = JsonResponse({'status': False, 'result': "unable to delete this image"})
        return y



@api_view(['GET'])
def Add_GC_groups(request):
    if request.method == "GET":

        g = My_GC_Groups.objects.filter(group_name = request.GET['group_name'],group_created_by=request.user)
        if len(g) == 0:


            new_group = {
                'group_created_by':request.user,
                'group_name':request.GET['group_name'],
                'group_created_date' : datetime.datetime.now(),

            }

            y = My_GC_Groups.objects.create(**new_group)

            users_list = {
                'group_id':y.id,
                'group_emails_list':request.GET['group_emails_list'],
                'saved_emails_date':datetime.datetime.now(),

                }

            z = Group_users_list.objects.create(**users_list)
            if z:

                x = JsonResponse({'status': True, 'success': "New group '%s' created successfully"%(y.group_name)})
                return x

            else:
                x = JsonResponse({'status': False, 'error': "we have faced error"})
                return x
        else:
            x = JsonResponse({'status': False, 'error': " '%s' group is already exist,please try another"%(request.GET['group_name'])})
            return x


def My_gc_groups(request):
    l=[]
    emails_list = []
    d = {}
    x= My_GC_Groups.objects.filter(group_created_by = request.user)

    for i in x:
        y= Group_users_list.objects.filter(group_id = i.id)
        del emails_list[:]
        for j in y:
            d['group_id'] = str(j.group_id)
            d['group_name'] = str(i.group_name)
            s=j.group_emails_list
            if s.startswith('['):
                line = j.group_emails_list.strip('[]\n')
                list_of_strs = line.split(',')

                z=[i[1:-1] for i in list_of_strs]


                d['group_emails_list'] = z
                l.append(d.copy())

                d.clear()
                del z

            else:
                z=[]+[str(j.group_emails_list)]
                d['group_emails_list'] = z
                l.append(d.copy())

                d.clear()
                del z
            #del l[:]


    #return HttpResponse(l)
    return render(request,'my_gc_groups.html',{'result':l})

def My_gc_groups_api(request):
    x= My_GC_Groups.objects.filter(group_created_by = request.user)
    res=[]
    emails_list = []
    d = {}

    for i in x:
        y= Group_users_list.objects.filter(group_id = i.id)
        for j in y:
            d['group_id'] = str(j.group_id)
            d['group_name'] = str(i.group_name)
            if '[]\n' in j.group_emails_list:
                line = j.group_emails_list.strip('[]\n')
                list_of_strs = line.split(', ')
                del emails_list[:]
                for elem in list_of_strs:
                    emails_list.append(elem)
                d['group_emails_list'] = emails_list
            else:
                d['group_emails_list'] = j.group_emails_list
            res.append(d.copy())
            d.clear()
    r = JsonResponse({'status': True, 'result': res})
    return r
    #return HttpResponse(l)

def del_group(request,pk):
    x = get_object_or_404(My_GC_Groups,id = pk)
    x.delete()
    if x:
        y = JsonResponse({'status': True, 'result': " file has been deleted successfully"})
        return y
    else:
        y = JsonResponse({'status': False, 'result': "unable to delete this image"})
        return y
@login_required
def mycontent_search(request):
    if request.method == "GET":
        l_private=[]
        d_private={}
        l_public=[]
        d_public={}
        if 'videos' in request.GET:
            key = request.GET['keyword']
            x= Keywords.objects.filter(keys__icontains = key)
            l_private[:]
            l_public[:]
            d_private.clear()
            d_public.clear()
            for i in x:
                y=Upload.objects.filter(id = i.upload_id,file_type = "video",user = request.user,file_access_mode = "private")
                for j in y:
                    d_private['upload'] = j.upload
                    d_private['filename'] = j.upload.name
                    d_private['id']= j.id
                    d_private['uploaded_by']= j.user.first_name

                    l_private.append(d_private.copy())
                    d_private.clear()
                #return HttpResponse(y.upload)
            for j in x:
                z=Upload.objects.filter(id =j.upload_id,file_type = "video",file_access_mode = "public")

                for i in z:
                    d_public['upload'] = i.upload
                    d_public['filename'] = i.upload.name
                    d_public['id']= i.id
                    d_public['uploaded_by']= i.user.first_name
                    l_public.append(d_public.copy())
                    d_public.clear()
            #return HttpResponse(y.upload)
            return render(request,'search_results.html',{"res_videos_private":l_private,"res_videos_public":l_public,"key":key})

        elif 'images' in request.GET :
            l_private[:]
            l_public[:]
            d_private.clear()
            d_public.clear()
            key = request.GET['keyword']
            x= Keywords.objects.filter(keys__icontains = key)

            for i in x:
                y=Upload.objects.filter(id = i.upload_id,file_type = "image",user = request.user,file_access_mode = "private")
                for j in y:
                    d_private['upload'] = j.upload
                    d_private['filename'] = j.upload.name
                    d_private['id']= j.id
                    d_private['uploaded_by']= j.user.first_name

                    l_private.append(d_private.copy())
                    d_private.clear()
                #return HttpResponse(y.upload)
            for j in x:
                z=Upload.objects.filter(id = j.upload_id,file_type = "image",file_access_mode = "public")
                for i in z:
                    d_public['upload'] = i.upload
                    d_public['filename'] = i.upload.name
                    d_public['id']= i.id
                    d_public['uploaded_by']= i.user.first_name

                    l_public.append(d_public.copy())
                    d_public.clear()
            #return HttpResponse(y.upload)
            return render(request,'search_results.html',{"res_images_private":l_private,"res_images_public":l_public,"key":key})


import json
@api_view(['GET','POST'])
def gc_login_api(request):
    if request.method == 'POST':
        
        if(request.POST.get('player')):
            #save auto sync metrics
            Last_Seen_Metrics.saveMetrics(request.POST.get('player'));

        x = User.objects.filter(username= request.POST.get("email"))
        if x:

            user=authenticate(request,username=request.POST.get("email"),password=request.POST.get("password"))
            d={}
            if user is not None :
                for i in x:
                    d["id"] = i.id
                    d["first_name"] = i.first_name
                    d["last_name"] = i.last_name
                    d["email"] = i.username

                    unique_key = User_unique_id.objects.get(user_id = i.id)

                    d["user_unique_key"] = unique_key.user_unique_key

                r = JsonResponse({'status': True, 'res': d})
                return r

            else:
                r = JsonResponse({'status': False, 'res': "Please Enter Correct Password "})
                return r
        else:
            r = JsonResponse({'status': False, 'res': "Please Enter Valid Email Address "})
            return r
    else:
        return JsonResponse({'status': False, 'res': "Invalid request"});


def my_campaigns(request):
    multiple_campaign = {}
    m_campaign = []

    m= Multiple_campaign_upload.objects.filter(campaign_uploaded_by = request.user.id)

    if m:
        for i in m:
            multiple_campaign["id"] = i.id
            multiple_campaign["campaign_uploaded_by"] = i.campaign_uploaded_by
            multiple_campaign["campaign_name"] = i.campaign_name
            multiple_campaign["text_file"] = "https://www.greencontent.in{}".format(i.text_file.url)
            multiple_campaign["created_date"] = i.created_date
            multiple_campaign["updated_date"] = i.updated_date

            f = Multiple_campaign_files.objects.filter(Multiple_campaign = i.id)
            l = []
            del l[:]
            for i in f:

                c = "https://www.greencontent.in{}".format(i.mul_files.url)
                l.append(c)

            multiple_campaign["media_files"] = l

            m_campaign.append(multiple_campaign.copy())

            multiple_campaign.clear()

        return render(request,'my_campaigns.html',{'res': m_campaign})
        #r = JsonResponse({'status': True, 'res': m_campaign})
       # return r

    else:
        r = JsonResponse({'status': True, 'res': "No files found"})
        return r


import pandas as pd
@api_view(['GET'])

def campaign_downloads_api(request,p):

    multiple_campaign = {}
    m_campaign = []

    m= Multiple_campaign_upload.objects.filter(campaign_uploaded_by = p)

    if m:
        for i in m:
            multiple_campaign["campaign_uploaded_by"] = i.campaign_uploaded_by
            multiple_campaign["campaign_name"] = i.campaign_name
            multiple_campaign["text_file"] = "https://www.greencontent.in{}".format(i.text_file.url)


            import time
            t = pd.Timestamp(i.created_date)
            f= time.mktime(t.timetuple())* 1000

            multiple_campaign["created_date"] = f
            multiple_campaign["updated_date"] = f

            f = Multiple_campaign_files.objects.filter(Multiple_campaign = i.id)

            l = []
            del l[:]
            for i in f:
                c = i.mul_files.url
                p = c.split('/')[-1]
                l.append(p)

            multiple_campaign["media_files"] = l


            m_campaign.append(multiple_campaign.copy())

            multiple_campaign.clear()

        r = JsonResponse({'status': True,'campaigns':m_campaign})
        return r
    else:
        r = JsonResponse({'status': False,'campaigns':"No campaigns found" })
        return r

@api_view(['GET','POST'])
#@login_required
def campaign_upload_api(request):

    if request.method == "POST":

        text_file = request.data["text_file"]
        d= text_file.name
        camp_name = str(d).split('.')[0]

        cam_check = Multiple_campaign_upload.objects.filter(campaign_uploaded_by=str(request.data["user_id"]),campaign_name = str(camp_name))
        if len(cam_check) == 0:

            #unique_key = User_unique_id.objects.get(user_id = result["user_id"])
                #static_media_path = '/home/adskite/myproject/signagecms/media/campaigns/{}/'.format(camp_name)
            folder='/home/adskite/myproject/signagecms/media/campaigns/{}/{}'.format(str(request.data["secretid"]),camp_name)
            fs = FileSystemStorage(location=folder) #defaults to   MEDIA_ROOT
            d = Multiple_campaign_upload()
            d.campaign_uploaded_by = str(request.data["user_id"])
            d.campaign_name = camp_name
            file_n = fs.save(text_file.name, text_file)
            d.text_file = '/campaigns/{}/{}/{}'.format(str(request.data["secretid"]),camp_name,text_file.name)
            d.created_date = datetime.datetime.now()
            d.updated_date = datetime.datetime.now()
            d.save()

            '''for i in result["media_files"]:

                f = Multiple_campaign_files()
                f.Multiple_campaign = d.id
                med_sile_n = fs.save(i.name, i)
                f.mul_files = '/campaigns/{}/{}/{}'.format(unique_key.user_unique_key,camp_name,i.name)
                f.save()'''

            x = JsonResponse({'status': True, 'result': "Campaign Uploaded succesfully","path":folder,"camp_name":camp_name ,"camp_id":d.id})
            return x
        else:
            folder='/home/adskite/myproject/signagecms/media/campaigns/{}/{}'.format(str(request.data["secretid"]),camp_name)

            for i in cam_check:

                x = JsonResponse({'status': True, 'result': "Campaign already exist" ,"path":folder,"camp_id":i.id})
                return x


    else:
        x = JsonResponse({'status': False, 'result': "Request should be in post method" })
        return x

@api_view(['GET','POST'])
#@login_required
def campaign_upload_files_api(request):

    if request.method == "POST":
        media_file = request.data["media_file"]
        file_path = '/campaigns/{}/{}/{}'.format(str(request.data["secretid"]),str(request.data["camp_name"]),str(media_file.name))
        file_check  = Multiple_campaign_files.objects.filter(Multiple_campaign=str(request.data["camp_id"]),mul_files = file_path)

        if len(file_check) == 0:
            folder='/home/adskite/myproject/signagecms/media/campaigns/{}/{}'.format(str(request.data["secretid"]),str(request.data["camp_name"]))
            if os.path.exists(folder):

                fs = FileSystemStorage(location=folder) #defaults to   MEDIA_ROOT

                f = Multiple_campaign_files()
                f.Multiple_campaign = str(request.data["camp_id"])
                med_file_n = fs.save(media_file.name, media_file)
                f.mul_files = '/campaigns/{}/{}/{}'.format(str(request.data["secretid"]),str(request.data["camp_name"]),media_file.name)
                f.save()

                x = JsonResponse({'status': True, 'result': "File Uploaded succesfully" })
                return x
            else:
                folder='/home/adskite/myproject/signagecms/media/campaigns/{}/{}'.format(str(request.data["secretid"]),str(request.data["camp_name"]))

                x = JsonResponse({'status': True, 'result': " path does not exist" ,"path":folder})
                return x

        else:
            x = JsonResponse({'status': True, 'result': " {} already exist ".format(media_file.name)})
            return x


    else:
        x = JsonResponse({'status': False, 'result': "Request should be in post method" })
        return x





from django.core.mail import send_mail
from accounts.models import ForgotPwdSession

def forgot_password(request):
    if request.method == "POST":
        email = request.POST['email'];
        email_check = User.objects.filter(username = email)
        if email_check:
            session = ForgotPwdSession.createSession(email_check[0].id);
            subject = 'Green Content Reset Password'
            message = 'https://www.greencontent.in/reset_password/{}/{}'.format(email,session)
            from_email = settings.EMAIL_HOST_USER
            to_list= []
            to_list.append(request.POST['email'])
            send_mail(subject, message, from_email,to_list,fail_silently=True)

            #return HttpResponse("we have sent a link to your registered email, please check it once ")
            return render(request,'forgot_password.html',{"success":"We have sent a password link to your registered email, please check it "})
        else:
            return render(request,'forgot_password.html',{"error":"Please enter valid email address "})
    else:
        return render(request,'forgot_password.html')

def reset_password(request,k,session):
    #check for session
    try:
        users = User.objects.filter(email=k);
        if(users):
            user = users[0];
            ForgotPwdSession.objects.get(user_id=user.id,session_key=session);
            if(request.method=="GET"):
               return render(request,'reset_password.html',{"id":k,"session":session}); 
            elif(request.method=="POST"):
                if request.POST["pass"] == request.POST["confirm_pass"]:
                    #u = User.objects.get(id=k)
                    user.set_password(request.POST["pass"])
                    user.save()
                    return render(request,'reset_password.html',{"success": "Your password is updated successfully","id":k,"session":session})
                    #return HttpResponse("your password is updated successfully ")

                else:
                    #return JsonResponse({'status',"Invalid password"})
                    return render(request,'reset_password.html',{"id":k,"session":session,"error": "Password must be same"})

        else:
            return redirect('/accounts/signin/')
    except ForgotPwdSession.DoesNotExist:
        return render(request,'forgot_password.html',{"error":"Session expired, please try again later"}); 



def all_user_emails_api(request):
    emails = []
    u = User.objects.all()
    for i in u:
        emails.append(i.email)

    x = JsonResponse({'status': True, 'result': emails })
    return x
























'''def addpost(request):
    if request.method == 'POST':
        post= request.POST['text']

        data=Post()
        data.post= post
        data.posted_by = request.user
        data.posted_time= datetime.datetime.now()
        data.save()

        return redirect('/queries/')


def editprofile(request):
    user = request.user
    if request.method == 'POST':
        userform=UserForm(request.POST,instance=user)
        profileform=ProfileForm(request.POST,files=request.FILES,instance=user.profile)
        if userform.is_valid() and profileform.is_valid():
            userform.save()
            profileform.save()

            messages.success(request, 'your profile is updated successfully')

            return redirect('/queries/')
        else:
            form1 = UserForm(instance=user)
            form2 = ProfileForm(instance=user.profile)
            messages.success(request, 'please enter valid data')

            return render(request, 'editprofile.html', {'UserForm': form1, 'ProfileForm': form2})
    else:
        form1 = UserForm(instance=user)

        form2 = ProfileForm(instance=user.profile)
        print request.user.profile.profile_pic

        print user.last_name
        return render(request,'editprofile.html',{'UserForm':form1,'ProfileForm': form2})

def change_password(request):
    if request.method == 'POST':
        form=ChangepasswordForm(request.POST)
        if form.is_valid():
            if check_password(form.cleaned_data['Old_password'], request.user.password):
                if form.cleaned_data['New_password'] == form.cleaned_data['Confirm_Newpassword']:
                    user = request.user
                    user.set_password(form.cleaned_data['New_password'])
                    user.save()
                    logout(request)
                    messages.success(request, 'your password is updated successfully. ')
                    return redirect('/queries/login/')

                else:
                    messages.error(request, 'password must be same')
                    form = ChangepasswordForm()
                    return render(request, 'change_password.html', {'form': form})

            else:
                messages.error(request, 'you enterd old password is wrong. please give correct details')
                form = ChangepasswordForm()
                return render(request, 'change_password.html', {'form': form})
    else:
        form=ChangepasswordForm()
        return render(request,'change_password.html',{'form':form})



def delete_comment(request,id):
    comment=get_object_or_404(Comments,pk=id)
    Comments.objects.get(id=id).delete()
    data = Post.objects.filter(id=comment.post_details_id)
    data2 = Comments.objects.filter(post_details=comment.post_details).order_by('-id')
    # print data.ccount()
    form = CommentsForm()
    #return HttpResponse(data1)
    messages.success(request, 'your comment is deleted successfully')

    return render(request, 'all_answers.html', {'commentform': form, 'post': data, 'comment': data2})

def delete_post(request,id):
    comment=get_object_or_404(Post,pk=id)
    Post.objects.get(id=id).delete()
    return redirect('/queries/')




def adskite(request):
    return render(request,'adskite_bot.html')

def hotel_booking(request):
    return render(request,'hotel_booking.html')

def course_details(request):
    return render(request,'course-details.html')

def weather_details(request):
    return render(request,'weather-details.html')

def sample(request):
    #x=str(data)
    return HttpResponse('raheem')'''

import os
from django.conf import settings
from django.http import HttpResponse, Http404
def downloadSoftIOT(request):
    if(request.user.is_authenticated==False):
       return redirect('/accounts/signin/?next=/download_softiot')

    fileName='soft_iot.apk';
    file_path = os.path.join(settings.MEDIA_ROOT, fileName)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh, content_type="application/vnd.android.package-archive") 
            response["Content-disposition"] = "attachment; filename={}".format(os.path.basename(file_path))
            return response
    raise Http404
    #return JsonResponse({'status':'inside download soft iot'});