var campaignId;

function initLocalUpload()
{
	if(info!=null && campaignInfoFile!=null)
  {
    
    displayInitUploadBusyDialog();
  

    var xhr = new XMLHttpRequest();
    var params = 'accessToken=web&info='+info+'&campaign='+campaignName+'&size='+size+
    '&store_location='+storeLocation;
    
    xhr.onload = function() {
        if (xhr.status === 200) {
        	console.log(xhr.response);
            var responseObj = JSON.parse(xhr.response);
            // Upload succeeded. Do something here with the file info.
            dismissInitBusyDialog();

            if(responseObj.statusCode == 0)
            {
               uploadPath = responseObj.save_path;
               campaignId= responseObj.cId;
               console.log("uploadPath"+uploadPath);
               uploadFileLocal(uploadFiles[0]);
            }else
            {
              dismissBusyDialog();
              swal(responseObj.status);
            }
            
        }
        else {
            var errorMessage = xhr.response || 'Unable to upload file';
            // Upload failed. Do something here with the error.
            console.log(errorMessage);
            swal("unable to upload - "+errorMessage);
        }
    };

    xhr.open('POST', '/campaigns/init/');
     
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

    xhr.setRequestHeader("X-CSRFToken", csrf_token);
    xhr.send(params);
  
  }else
  {
    swal("Please select campaign");
  }
  return false;
}

function uploadFileLocal(file) {
    
    //init upload file dialog
    initUploadFileBusyDialg();  
    //init update state
    uploadState.file = file;

    uploadViaHttpLocal(file); 
     
      return false;
}

function uploadViaHttpLocal(file)
{
    var xhr = new XMLHttpRequest();
    var isInitial = true;
    var totalSizeInstr = formatBytes(file.size,3);
    xhr.upload.onprogress = function(evt) {
  
        var percentComplete = parseInt(100.0 * evt.loaded / evt.total);
        // Upload in progress. Do something here with the percent complete.
        updateFileProgressBusyDialog(percentComplete,formatBytes(evt.loaded,3)+"/"+totalSizeInstr);

        if(isInitial)
        {
          dismissInitFileUploadBusyDiag();
          isInitial = false;
        }
       
    };

  xhr.onload = function() {
      if (xhr.status === 200) {
          var uploadResponse = JSON.parse(xhr.response);
          // Upload succeeded. Do something here with the file info.
          if(uploadResponse['statusCode']==0)
          {
            
            checkAndUploadNextFileLocal();
          }else
          {
            uploadInterruptLocal("Upload failed"+errorMessage);
          }
          
      }
      else {
          var errorMessage = xhr.response || 'Unable to upload file';
          // Upload failed. Do something here with the error.
          
          uploadInterruptLocal("Upload failed"+errorMessage);
      }
  };
 

  xhr.onerror = function()
  {
    
    //alert('Unable to upload, please check your connections');
    uploadInterruptLocal('Unable to upload, please check your connections');
  };
  
   xhr.open('post', '/campaigns/uploadCampaignResource/', true);
   xhr.setRequestHeader("X-CSRFToken", csrf_token);
            var fd = new FormData();
            fd.append("access_token", 'web');
            fd.append("file", file);
            fd.append("file_name",getUploadFileName(file.name))
            fd.append("c_id", campaignId);
            xhr.send(fd);
}

function checkAndUploadNextFileLocal()
{
  ++uploadingFilePos;
  
  if(uploadFiles.length > uploadingFilePos)
  {
    uploadFileLocal(uploadFiles[uploadingFilePos]);
  }else
  {
    dismissBusyDialog();
      swal({
    title: "Campaign has been created successfully!",
    text: "Redirecting in 2 seconds.",
    type: "success",
    timer: 2000,
    showConfirmButton: false
  }, function(){
        window.location.href = "/campaigns/list_camp_web";
  });
    
  }
}

function uploadInterruptLocal(warningMsg)
{

   var isConfirm = confirm(warningMsg+"\n"+"\t Would you like to retry?");
  if(isConfirm)
  {
     //retry uploading
     
     retryUploadLocal();
  }else{
    dismissBusyDialog();
    location.reload();
  }
}

function retryUploadLocal()
{
  var uploadingFile = uploadState.file;
  if(uploadingFile==null || uploadingFile == undefined)
  {
   reUploadFileLocal();

  }else if(uploadingFile.size < UPLOAD_FILE_SIZE_LIMIT)
  {
    reUploadFileLocal();
  }else{
     //reUploadLargeFileChunks(uploadingFile);
    reUploadFileLocal();
  }
}

function reUploadFileLocal()
{
   
    if(uploadFiles.length > uploadingFilePos)
    {
      uploadFileLocal(uploadFiles[uploadingFilePos]);
    }
}
