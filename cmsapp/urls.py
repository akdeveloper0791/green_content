from django.conf.urls import url
from django.urls import path

from cmsapp import views
from campaign import views as cView


urlpatterns = [

        url(r'^$',cView.listCampaignsWeb,name='listCampaignsWeb'),
        url(r'^home/$',cView.listCampaignsWeb,name='listCampaignsWeb'),
        url(r'^mycontent/$',cView.listCampaignsWeb,name='listCampaignsWeb'),
        url(r'^web_search/$',views.web_search,name='web_search'),
        url(r'^signageserv/$',views.signageserv,name='signageserv'),
        url(r'^search/$',cView.listCampaignsWeb,name='listCampaignsWeb'),



        url(r'^logout/$', views.signout, name='logout'),
        url(r'^result/',views.search,name='result'),

        url(r'^all_content/',views.all_content,name='all_content'),

        url(r'^youtube_content/$', views.youtube_content, name='youtube_content'),
        url(r'^images_content/$', views.images_content, name='images_content'),
        url(r'^news_content/$', views.news_content, name='news_content'),

        url(r'^my_wishlist/$', views.my_wishlist, name='my_wishlist'),
        url(r'^my_videos/', views.my_videos, name='my_videos'),
        url(r'^my_images/', views.my_images, name='my_images'),
        url(r'^my_news/', views.my_images, name='my_images'),

        url(r'^videos_remove/(\d+)/$', views.videos_remove, name='videos_remove'),
        url(r'^images_remove/(\d+)/$', views.images_remove, name='images_remove'),
        url(r'^news_remove/(\d+)/$', views.news_remove, name='news_remove'),
        url(r'^login_auth/', views.login_auth, name='login_auth'),
        url(r'^video_upload/', views.video_upload, name='video_upload'),
        url(r'^video_upload/', views.video_upload, name='video_upload'),
        url(r'^images_upload/', views.images_upload, name='images_upload'),
        url(r'^downloads_videos/(\d+)/$', views.downloads_videos, name='downloads_videos'),
        url(r'^downloads_images/(\d+)/$', views.downloads_images, name='downloads_images'),

        url(r'^about_us/$',views.about_us,name='about_us'),

        url(r'^terms_services/$',views.terms_services,name='terms_services'),

        url(r'^privacy_services/$',views.privacy_services,name='privacy_services'),

         url(r'^contact_us/$',views.contact_us,name='contact_us'),

        url(r'^api_videos/$',views.api_videos,name='api_videos'),
        url(r'^api_images/$',views.api_images,name='api_images'),


        url(r'^my_content/', views.my_content, name='my_content'),

        url(r'^mycontent_images/', views.mycontent_images_api, name='mycontent_images'),
        url(r'^mycontent_videos/', views.mycontent_videos_api, name='mycontent_videos'),
        url(r'^downloads_upload_files/(\d+)/$', views.downloads_upload_files, name='downloads_upload_files'),
        url(r'^remove_upload_files/(\d+)/$', views.remove_upload_files, name='remove_upload_files'),

        url(r'^My_GC_Groups/', views.My_gc_groups, name='My_GC_Groups'),

        url(r'^My_GC_Groups_Api/', views.My_gc_groups_api, name='My_GC_Groups_Api'),

        url(r'^mycontent_search/', views.mycontent_search, name='mycontent_search'),
        url(r'^Add_GC_groups/', views.Add_GC_groups, name='Add_GC_groups'),

        url(r'^edit_upload/(\d+)/$', views.edit_upload, name='edit_upload'),
        url(r'^edit_upload_post/(\d+)/$', views.edit_upload_post, name='edit_upload_post'),

        url(r'^del_group/(\d+)/$', views.del_group, name='del_group'),

        url(r'^campaign/', views.campaign_upload, name='campaign_upload'),

        url(r'^single_campaigns/', views.single_campaign_preview, name='single_campaign'),

        url(r'^gc_login_api/', views.gc_login_api, name='gc_login_api'),

        url(r'^my_campaigns/', views.my_campaigns, name='my_campaigns'),

        url(r'^campaign_downloads_api/(\d+)/$', views.campaign_downloads_api, name='campaign_downloads_api'),

        url(r'^forgot_password/', views.forgot_password, name='forgot_password'),
        
        path('reset_password/<k>/<session>', views.reset_password, name='reset_password'),

        #url(r'^reset_password/(\d+)/$', views.reset_password, name='reset_password'),

        url(r'^all_user_emails_api/', views.all_user_emails_api, name='all_user_emails'),



        url(r'^campaign_upload_api/$', views.campaign_upload_api, name='campaign_upload_api'),

        url(r'^campaign_upload_files_api/$', views.campaign_upload_files_api, name='campaign_upload_files_api'),

        path('download_softiot',views.downloadSoftIOT,name="downloadSoftIOT"),

        url(r'^api_documentation/', views.apiDocumentation, name='apiDocumentation'),
        
        path('download_dsp',views.downloadDSP,name="downloadDSP"),

]


