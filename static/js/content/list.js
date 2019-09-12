var uploadDXXX = [];
var downloadThumbs = [];
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

function downloadThumbFile()
{
  console.log("downloadThumbInfo.store_location"+downloadThumbInfo.store_location);
   var resourceFile = downloadThumbInfo.resourceName;
  if(downloadThumbInfo.store_location == 1)//local
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

function deleteContent(contentId,campName)
 {

   swal({
            title: "Are you sure?",
            text: "You want to delete content",
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "Yes, delete it!",
            closeOnConfirm: false
        },
         function(isConfirm){
           if (isConfirm) {
    
    ajaxindicatorstart("Please wait");
   var xhr = new XMLHttpRequest();
   xhr.onload = function() {
      if (xhr.status === 200) {
        ajaxindicatorstop();
          console.log("xhr.response"+xhr.response);
          var response = JSON.parse(xhr.response);       
          try
          {
             if(response.statusCode==0)
             {
              
              deleteCampaignRow(contentId);
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
  xhr.open('POST', '/content/delete');
  xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  xhr.setRequestHeader("X-CSRFToken", csrf_token);
  
  
  var params = 'accessToken=web&c_id='+contentId+'&mac=web';
   
   xhr.send(params);
   }else{
                swal("Cancelled", "Your imaginary file is safe :)", "error");
          } 
    });
 }

 function deleteError(msg)
 {
   ajaxindicatorstop();
   alert(msg);
 }

 function deleteCampaignRow(campaignId)
 {
   document.getElementById("content_list_table").deleteRow(document.getElementById('content_title_'+campaignId).rowIndex);
   document.getElementById("content_list_table").deleteRow(document.getElementById('content_title2_'+campaignId).rowIndex);
 }