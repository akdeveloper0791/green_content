var uploadDXXX = [];
var downloadThumbs = [];
//downlod campaign
function download(id,storeLocation,
    	campaignName,savePath){
    	
    	
    	if(storeLocation==2)//download from drop box
    	{
    		//downloadFromDropBox(campaignName);

      checkForFilesInDropBox(campaignName,savePath);
    	}else
    	{
    		//download FROM GC 
    	}
      
}


function checkForFilesInDropBox(campaignName,savePath)
{


   displayInitUploadBusyDialog();
  
  if(uploadDXXX!=null && Object.keys(uploadDXXX).length>=1)
  {
   var xhr = new XMLHttpRequest();
   
   xhr.onload = function() {
      if (xhr.status === 200) {
         
          var fileInfo = JSON.parse(xhr.response);
         
          downloadDropboxCamp(campaignName,savePath);
         // checkAndUploadNextFile();
      }
      else {
          var errorMessage = xhr.response;
           ;
          // Upload failed. Do something here with the error.
          if(errorMessage)
          {
            try
            {
              var jsonObj = JSON.parse(errorMessage);

              if(jsonObj.error_summary.indexOf("path/not_found") !== -1)
              {
                interrupt("No campaign files found");
              }else{
                interrupt('Unable to download please try again later -'+errorMessage);
              }
            }catch(exception)
            {
              interrupt('Unable to download please try again later -'+errorMessage);
            }
            
            
          }else{
            interrupt('Unable to download please try again later');
          }
         
          
         // uploadInterrupt("Upload failed"+errorMessage);
      }
  };
  
  xhr.onerror = function()
  {
    
    
    interrupt('Unable to download, please check your connections');
  };

  xhr.open('POST', 'https://api.dropboxapi.com/2/files/get_metadata');
  xhr.setRequestHeader('Authorization', 'Bearer ' + uploadDXXX['xxdd']);

  xhr.setRequestHeader('Content-Type', 'application/json');

  // xhr.setRequestHeader('Dropbox-API-Arg', JSON.stringify({
  //     path: '/'+uploadPath+  file.name,
  //     mode: 'add',
  //     autorename: true,
  //     mute: false
  // }));
  var params = JSON.stringify({"path":savePath+
    campaignName+".txt",
    "include_media_info": false,
    "include_deleted": false,
    "include_has_explicit_shared_members": false})
  xhr.send(params);
 }else
  {
         initUploadDxxx(campaignName,savePath);
  }
}



function initUploadDxxx(campaignName,savePath)
  {
    var xhr = new XMLHttpRequest();
    

    xhr.onload = function() {
      
        if (xhr.status === 200) {
            uploadDXXX = JSON.parse(xhr.response);
            
            downloadThumbFile();
        }
        else {
          var errorMessage = xhr.response || 'Unable to download file';
            
            //initUploadDBxxFail("Downloading failed"+errorMessage);
        }
    };
    xhr.onerror = function()
    {
      
      //alert('Unable to upload, please check your connections');
      //initUploadDBxxFail('Unable to download, please check your connections');
    };
   
    xhr.open('POST', '/gdbx/init/');
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

    xhr.setRequestHeader("X-CSRFToken", csrf_token);
    var params = 'accessToken=web';
    xhr.send(params);
  }

  function initUploadDBxxFail(warningMsg)
{
  swal(warningMsg);
  dismissBusyDialog();
  
}

function interrupt(errorMsg)
{
  dismissBusyDialog();
  swal(errorMsg);
}

function str2bytes (str) {
   var bytes = new Uint8Array(str.length);
   for (var i=0; i<str.length; i++) {
      bytes[i] = str.charCodeAt(i);
    }
    return bytes;
}

function downloadDropboxCamp(campaignName,savePath)
{
  
   var params = JSON.stringify({"path":savePath,
   });
   
  var xhr = new XMLHttpRequest();
  
   xhr.open('POST', 'https://content.dropboxapi.com/2/files/download_zip');
   xhr.setRequestHeader('Authorization', 'Bearer ' + uploadDXXX['xxdd']);

   xhr.setRequestHeader('Dropbox-API-Arg', params);

    xhr.onload = function() {
      if (xhr.status === 200) {
        
           var blob = new Blob([xhr.response], {type: "octet/stream"});
        var fileName = campaignName+".zip";
        var a = document.createElement("a");
            document.body.appendChild(a);
            a.style = "display:none";
            var url = window.URL.createObjectURL(blob);
            a.href = url;
            a.download = fileName;
            a.click();

            window.URL.revokeObjectURL(url);
            a.remove();
          dismissBusyDialog();
      }
      else {
          var errorMessage = xhr.response;
           ;
          // Upload failed. Do something here with the error.
          if(errorMessage)
          {
            try
            {
             
                interrupt('Unable to download please try again later -'+errorMessage);
              
            }catch(exception)
            {
              interrupt('Unable to download please try again later -'+errorMessage);
            }
            
            
          }else{
            interrupt('Unable to download please try again later');
          }
         
          
         // uploadInterrupt("Upload failed"+errorMessage);
      }
  };
  
  xhr.onerror = function()
  {
    
    
    interrupt('Unable to upload, please check your connections');
  };
  
 xhr.upload.onprogress = function(evt) {

      
        var percentComplete = parseInt(100.0 * evt.loaded / evt.total);

       
      };


 xhr.responseType = "arraybuffer";
  xhr.send();

}

function checkAndDownloadThumbFile()
{
   var hasThumbs = getDownloadThumbInfo();
   if(hasThumbs)
   {
    
    downloadThumbFile();
   }else{
    console.log("Downloading thumbs finished");
   }
}

//download thumb nails
function downloadThumbFile()
{
  var resourceFile = "DNDM-THUMB-"+downloadThumbInfo.resourceName+".jpg"

  if(downloadThumbInfo.camp_type==3)
  {
         document.getElementById('thumb_img_'+downloadThumbInfo.id).src = 
         '/static/images/campaign/ticker_text.png';
        checkAndDownloadThumbFile();
  }
  else if(downloadThumbInfo.store_location == 1)//local
  {
    var url = "/media"+downloadThumbInfo.save_path+resourceFile;
    updateThumbPreview(url);
    
  }else{ //drop box
  if(uploadDXXX!=null && Object.keys(uploadDXXX).length>=1)
  {
    {
     
     var xhr = new XMLHttpRequest();
      xhr.onload = function() {
        if (xhr.status === 200) {
            
            var fileInfo = JSON.parse(xhr.response);
          
            try
            {
              var list = fileInfo.links;
              if(list.length>=1)
              {
                link = list[0];
                var url = link['url'];
                updateThumbPreview(url);
              }else{
                
                generateNewLink(resourceFile);
              }
            }catch(exception)
            {

              checkAndDownloadThumbFile();
              //childPreviewError(resourceId,'Unable to display preview, please try again later -'+exception.message);
            }
            
        }
        else {
            var errorMessage = xhr.response;
             checkAndDownloadThumbFile();
                  //childPreviewError(resourceId,'Unable to display preview-'+errorMessage);
           
            }
    };
    xhr.onerror = function()
    {
      
      checkAndDownloadThumbFile();
     //childPreviewError(resourceId,'No internet');
    };
    xhr.open('POST', 'https://api.dropboxapi.com/2/sharing/list_shared_links');
    
    xhr.setRequestHeader('Authorization', 'Bearer ' + uploadDXXX['xxdd']);

    xhr.setRequestHeader('Content-Type', 'application/json');

    
    var params = JSON.stringify({"path":downloadThumbInfo.save_path+resourceFile,
      })
     
       

     xhr.send(params);
   }
  }else
   {
         initUploadDxxx();
   }
  }
 }

 //generate new link
 function generateNewLink(resourceFile)
 {
  
   var xhr = new XMLHttpRequest();
    xhr.onload = function() {
      if (xhr.status === 200) {
         
        var fileInfo = JSON.parse(xhr.response);
        

          try
          {
            var url = fileInfo.url;
            
            updateThumbPreview(url);
            
          }catch(exception)
          {
            checkAndDownloadThumbFile();
          }
          
      }
      else {
          var errorMessage = xhr.response;
           
           checkAndDownloadThumbFile();
         
          }
  };
  xhr.onerror = function()
  {
    
    
   checkAndDownloadThumbFile();
  };
  
  xhr.open('POST', 'https://api.dropboxapi.com/2/sharing/create_shared_link_with_settings');
  
  xhr.setRequestHeader('Authorization', 'Bearer ' + uploadDXXX['xxdd']);

  xhr.setRequestHeader('Content-Type', 'application/json');

  
  var params = JSON.stringify({"path":downloadThumbInfo.save_path+resourceFile,
     "settings": {
        "requested_visibility": "public"
         }
    });
   
  xhr.send(params);
 }

 function updateThumbPreview(url)
 {
   //reform url to display preview
   var res = url.split("?");
   url = res[0]+"?raw=1";
   document.getElementById('thumb_img_'+downloadThumbInfo.id).src = url;
   checkAndDownloadThumbFile();
 }

 function deleteCampaign(campaignId,campName)
 {

   swal({
            title: "Are you sure?",
            text: "You want to delete campaign\nCampaign name:"+campName,
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "Yes, delete it!",
            closeOnConfirm: false
        },
         function(isConfirm){
           if (isConfirm) {
    
    displayInitUploadBusyDialog();
   var xhr = new XMLHttpRequest();
   xhr.onload = function() {
      if (xhr.status === 200) {
        dismissBusyDialog();
          
          var response = JSON.parse(xhr.response);       
          try
          {
             if(response.statusCode==0)
             {
              
              deleteCampaignRow(campaignId);
                {
                 
                 swal({
                 title: "Deleted succesfully!",
                 text: "",
                 type: "success",
                 timer: 3000   
                 });
                }
             }else{
              deleteError(response.status);
             }
          }catch(exception)
          {

            deleteError('Unable to delete -'+exception.message);
          }
          
      }
      else {
           var errorMessage = xhr.response;
           deleteError('Unable to delete-'+errorMessage);
         
          }
  };
  xhr.onerror = function()
  {
    deleteError('No internet');
  };
  xhr.open('POST', '/campaigns/delete_campaign/');
  xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  xhr.setRequestHeader("X-CSRFToken", csrf_token);
  
  
  var params = 'accessToken=web&camp_id='+campaignId+'&mac=web';
   
   xhr.send(params);
   }else{
                swal("Cancelled", "Your imaginary file is safe :)", "error");
          } 
    });
 }

 function deleteError(msg)
 {
   dismissBusyDialog();
   alert(msg);
 }

 function publishCampaign(campaignId)
 {
   lptpPublishCampaign(campaignId);
 }

 function deleteCampaignRow(campaignId)
 {
   document.getElementById("campaign_list_table").deleteRow(document.getElementById('campaign_title_'+campaignId).rowIndex);
   document.getElementById("campaign_list_table").deleteRow(document.getElementById('campaign_title2_'+campaignId).rowIndex);
 }


 function getCampaignInfoToEdit(campaignId)
{

  try {
        ajaxindicatorstart("<img src='/static/images/ajax-loader.gif'><br/> Please wait...!");
       
    $.ajax(
    {

      type:'POST',
      url: '/campaigns/getEditCampaignInfo/',
      headers: {            
            'X-CSRFToken': csrf_token
        },
      data:{
                accessToken: 'web',
                c_id: campaignId,
                
      },
      
      success: function(data)
       {
         ajaxindicatorstop();
      console.log("getCampaignInfoDialog:"+JSON.stringify(data));
            
            if(data['statusCode']==0)
        {
             
          displayCamapignEditDialog(data,campaignId);
            
        }
      else
      {

             swal(data['status']);
                                    
      }

       },
    
     error: function (jqXHR, exception) {
      ajaxindicatorstop();
      alert(exception+jqXHR.responseText);
     }

    });
  }
  catch(Exception)
    {
    alert(Exception.message);
  } 
}


 function displayCamapignEditDialog(data,campaignId)
 {
   document.getElementById('campaign_edit_dialog').style.display="block";

  document.getElementById('camp_id').value=campaignId;
  document.getElementById('camp_name').innerHTML=data['campaign_name'];
  document.getElementById('duration_id').value=data['duration'];
  var flag=data['hide_ticker_txt'];
  //var isTrueSet =(flag === 'true');
  console.log("hide_ticker_txt"+flag);
  document.getElementById('hide_ticker').checked=flag;

   if(data.hasOwnProperty('media_name'))
   {
    //In the array!
    document.getElementById('text_block').style.display="block";
    document.getElementById('ticker_text').value=data['media_name'];

    }else
    {
    document.getElementById('text_block').style.display="none";
     var mediaName=""; 
    } 
 }

 function closeCampaignEditDialog()
 {
  document.getElementById('campaign_edit_dialog').style.display="none";
 }

 function editCamapignInfo()
 {
  var campDuration=document.getElementById('duration_id').value;
  var hideTickerFlag=document.getElementById('hide_ticker').checked;

   mediaName=document.getElementById('ticker_text').value;
 if(mediaName==null || mediaName.trim()=='' || mediaName<=0 )
  {  
      swal("Please enter valid text"); 
 
  }

   if(campDuration==null || campDuration.trim()=='' || campDuration<=0 )
  {  
      swal("Please enter valid duration"); 
 
  }else
    {
      if(campDuration<10)
    {
   swal("Campaign duration is greater than 10 sec.");
    }else
    {
      updateCampignInfo(campDuration,hideTickerFlag,mediaName);
    }
   }

 }

 function updateCampignInfo(campDuration,hideTickerFlag,mediaName)
 {
  
 try {
   ajaxindicatorstart("<img src='/static/images/ajax-loader.gif'><br/> Please wait...!");    
    $.ajax(
    {

      type:'POST',
      url: '/campaigns/editCampaign/',
      headers: {            
            'X-CSRFToken':csrf_token
        },
      data:{
           accessToken: 'web',
             c_id: document.getElementById('camp_id').value,
             duration: campDuration,
             hide_ticker_txt: hideTickerFlag,
             media_name: mediaName,   
      },
     
      success: function(data)
       {
        ajaxindicatorstop();
        if(data['statusCode']==0)
        {
          mediaName="";
          closeCampaignEditDialog();
          showSnackbar(data['status']);
        }
        
       else
       {
        swal(data['status']);                           
       }

       },
    
     error: function (jqXHR, exception) {
      console.log(jqXHR.responseText);
      ajaxindicatorstop();
      swal(exception+jqXHR.responseText);
     }

    });
    }
      catch(Exception)
      {
        ajaxindicatorstop();
        swal(Exception.message);
      }
 }

 function showSnackbar(message) {
  var x = document.getElementById("snackbar");
  x.innerHTML=message;
  x.className = "show";
  setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
}