var uploadDXXX = [];
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
            
            checkForFilesInDropBox(campaignName,savePath);
        }
        else {
          var errorMessage = xhr.response || 'Unable to download file';
            
            initUploadDBxxFail("Downloading failed"+errorMessage);
        }
    };
    xhr.onerror = function()
    {
      
      //alert('Unable to upload, please check your connections');
      initUploadDBxxFail('Unable to download, please check your connections');
    };
   
    xhr.open('POST', '/gdbx/init/');
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

    xhr.setRequestHeader("X-CSRFToken", csrf_token);
    var params = 'accessToken=web';
    xhr.send(params);
  }

  function initUploadDBxxFail(warningMsg)
{
  alert(warningMsg);
  dismissBusyDialog();
  
}

function interrupt(errorMsg)
{
  dismissBusyDialog();
  alert(errorMsg);
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