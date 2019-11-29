DROP_BOX_ACCESS_TOKEN = "mkW1hX251tAAAAAAAAAK8TvQzlCj0VwXFCAyHAWCI18CNSpPNDU4a1EUC6Xxt3R9"
API_HOST = "https://www.greencontent.in"
ADSKITE_PLAYER_REGISTER_PWD="!AdsKite2019$"
SINGLE_100_100 = "{\"regions\":[{\"width\":100,\"height\":100,\"top_margin\":0,\"left_margin\":0,\"right_margin\":0,\"bottom_margin\":0}]}"
one_reg_vertical_json = "{\"regions\":[{\"width\":100,\"height\":90,\"top_margin\":0,\"left_margin\":0,\"right_margin\":0,\"bottom_margin\":0},{\"width\":100,\"height\":10,\"top_margin\":90,\"left_margin\":0,\"right_margin\":0,\"bottom_margin\":0}]}"
two_reg_vertical_json = "{\"regions\":[{\"width\":100,\"height\":90,\"top_margin\":0,\"left_margin\":0,\"right_margin\":0,\"bottom_margin\":0},{\"width\":100,\"height\":10,\"top_margin\":90,\"left_margin\":0,\"right_margin\":0,\"bottom_margin\":0}]}"
two_reg_hoirz_json = ''' {"regions":[{"width":50,"height":100,"top_margin":0,"left_margin":0,"right_margin":0,"bottom_margin":0},{"width":50,"height":100,"top_margin":0,"left_margin":50,"right_margin":0,"bottom_margin":0}]} '''
two_horiz_one_below_json = ''' {"regions":[{"width":50,"height":90,"top_margin":0,"left_margin":0,"right_margin":0,"bottom_margin":0},{"width":50,"height":90,"top_margin":0,"left_margin":50,"right_margin":0,"bottom_margin":0},{"width":100,"height":10,"top_margin":90,"left_margin":0,"right_margin":0,"bottom_margin":0}]} '''
two_reg_vertical_50_50_json = ''' {"regions":[{"width":100,"height":50,"top_margin":0,"left_margin":0,"right_margin":0,"bottom_margin":0},{"width":100,"height":50,"top_margin":50,"left_margin":0,"right_margin":0,"bottom_margin":0}]} '''
two_vertical_20_70_json = ''' {"regions":[{"width":100,"height":10,"top_margin":0,"left_margin":0,"right_margin":0,"bottom_margin":0},{"width":100,"height":90,"top_margin":10,"left_margin":0,"right_margin":0,"bottom_margin":0}]} '''
r3_1h_2v_20_50_50_json = ''' {"regions":[{"width":100,"height":10,"top_margin":0,"left_margin":0,"right_margin":0,"bottom_margin":0},{"width":50,"height":90,"top_margin":10,"left_margin":0,"right_margin":0,"bottom_margin":0},{"width":50,"height":90,"top_margin":10,"left_margin":50,"right_margin":0,"bottom_margin":0}]} '''
r4_2h_2v_50_50_json = ''' {"regions":[{"width":50,"height":50,"top_margin":0,"left_margin":0,"right_margin":0,"bottom_margin":0},{"width":50,"height":50,"top_margin":0,"left_margin":50,"right_margin":0,"bottom_margin":0},{"width":50,"height":50,"top_margin":50,"left_margin":0,"right_margin":0,"bottom_margin":0},{"width":50,"height":50,"top_margin":50,"left_margin":50,"right_margin":0,"bottom_margin":0}]} '''
allowed_image_formats = '''jpeg,jpg,png'''
allowed_video_formats = '''wmv,avi,mpg,mpeg,webm,mp4'''

#apache/local
#file_storage_path="C:/Users/jitendra/python_projects/green_content/media";

#nginx docker
file_storage_path="media";

STORE_LOCATION =1; #2-> dropbox , 1-> local
setup = 1; #2 server, 1->local


project_local_path = "C:/Users/jitendra/python_projects/green_content"

project_server_path = "/home/adskite/myproject/signagecms"

#schedule types
schedule_always= 10
schedule_custom = 100

fcm_api_key = "AAAAABJU_OM:APA91bG3swWJ9xiiKjZNc_rkqLwNqzBud5MvPmD6uYIg8Axi6fKwmcwtZ1A8sVUBPKZCeRmFAXlLoUgzq_kvpcch04kRngp3vdPem8ozw_RWxAjG1LwTnY9m8ozTg04HyHJtKq38l282"
fcm_handle_metrics_rule="1";
fcm_handle_mic_rule = "2";

EMAIL_HOST_USER = "contact@adskite.com"

content_pagination_limit = 10;