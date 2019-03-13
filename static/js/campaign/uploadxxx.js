var uploadFiles = [];var campaignInfoFile=null;
var info = null; var campaignName = null;
var uploadPath = null; var uploadingFilePos =0; var size = 0;
var uploadState = {
    chunkSize: 1024 * 1024,
    cursor: undefined,
    current_chunk: 0,//churrent chunk uploading
    total_chunks: 0,//total chunks to upload
    file: null,
    session_id:null,blob:null
  };
const maxBlob = 8 * 1000 * 1000; // 8Mb - Dropbox JavaScript API suggested max file / chunk size
const UPLOAD_FILE_SIZE_LIMIT = 150 * 1024 * 1024;
var uploadDXXX = [];  
function clearGlobalVaribles()
 {
    uploadFiles.length =0;
    campaignInfoFile = null;
    info=null;campaignName=null;uploadPath=null;uploadingFilePos=0;size=0;
    
    uploadState = {chunkSize: 1024 * 1024,
    cursor: undefined,current_chunk: undefined,
    total_chunks: 0,file: null,session_id:null,blob:null };
  }

function formatBytes(bytes,decimals) {
   if(bytes == 0) return '0 Bytes';
   var k = 1024,
       dm = decimals <= 0 ? 0 : decimals || 2,
       sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
       i = Math.floor(Math.log(bytes) / Math.log(k));
   return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + '' + sizes[i];
}

 

  function uploadFile(file) {
    
    //init upload file dialog
    initUploadFileBusyDialg();

    
    //init update state
    uploadState.file = file;

    var dbx = new Dropbox.Dropbox({ accessToken: uploadDXXX['xxdd'] });
      
      if (file.size < UPLOAD_FILE_SIZE_LIMIT) { 
           uploadViaHttp(file,uploadDXXX['xxdd']);

         } else { // File is bigger than 150  Mb - use filesUploadSession* API
        
        var workItems = [];     
      
        var offset = 0;
        while (offset < file.size) {
          var chunkSize = Math.min(maxBlob, file.size - offset);
          workItems.push(file.slice(offset, offset + chunkSize));
          offset += chunkSize;
        } 
        
        uploadState.total_chunks = workItems.length;

        const task = workItems.reduce((acc, blob, idx, items) => {

         

          if (idx == 0) {
            // Starting multipart upload of file
            
            return acc.then(function() {
              return dbx.filesUploadSessionStart({ close: false, contents: blob})
                        .then(response => response.session_id)
            });          
          } else if (idx < items.length-1) {  
            // Append part to the upload session
            
            return acc.then(function(sessionId) {
            
            if(idx==1)
            {
              dismissInitFileUploadBusyDiag();
            }

            //update current chunk
            uploadState.current_chunk = idx;

            updatePercentageForlargeFile();

             var cursor = { session_id: sessionId, offset: idx * maxBlob };

             uploadState.session_id = sessionId;
             uploadState.cursor = cursor;

             return dbx.filesUploadSessionAppendV2({ cursor: cursor, close: false, contents: blob }).then(() => sessionId); 

            });
          } else {
          	
            // Last chunk of data, close session
            return acc.then(function(sessionId) {
            	
              //update current chunk
            uploadState.current_chunk = idx;

            updatePercentageForlargeFile();

              var cursor = { session_id: sessionId, offset: file.size - blob.size };

              uploadState.session_id = sessionId;
              uploadState.cursor = cursor;

              var commit = { path: uploadPath+getUploadFileName(file.name), mode: 'overwrite', autorename: false, mute: false };              
              return dbx.filesUploadSessionFinish({ cursor: cursor, commit: commit, contents: blob });           
            });
          }          
        }, Promise.resolve());
        
        task.then(function(result) {
         /* var results = document.getElementById('results');
          results.appendChild(document.createTextNode('File uploaded!'));*/

          checkAndUploadNextFile();

        }).catch(function(error) {
        
          //alert("Unable to upload error "+error);
          uploadInterrupt("Unable to upload error "+error);
        });
        
      }
     
     
      return false;
    }

  function initUploadDxxx()
  {
    var xhr = new XMLHttpRequest();
    

    xhr.onload = function() {
      
        if (xhr.status === 200) {
            uploadDXXX = JSON.parse(xhr.response);
            
            initUpload();
        }
        else {
          var errorMessage = xhr.response || 'Unable to upload file';
            
            initUploadDBxxFail("Upload failed"+errorMessage);
        }
    };
    xhr.onerror = function()
    {
      
      //alert('Unable to upload, please check your connections');
      initUploadDBxxFail('Unable to upload, please check your connections');
    };
   
    xhr.open('POST', '/gdbx/init/');
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

    xhr.setRequestHeader("X-CSRFToken", csrf_token);
    var params = 'accessToken=web';
    xhr.send(params);
  }
  
  function updatePercentageForlargeFile()
  {
    var percentComplete = parseFloat((uploadState.current_chunk/
      uploadState.total_chunks)*100.0);

    

    updateFileProgressBusyDialog(percentComplete,formatBytes(maxBlob*uploadState.current_chunk,3)+"/"+formatBytes(maxBlob*uploadState.total_chunks,3));

  }

  function uploadViaHttp(file,accessToken)
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
	        var fileInfo = JSON.parse(xhr.response);
	        // Upload succeeded. Do something here with the file info.
	        
          checkAndUploadNextFile();
	    }
	    else {
	        var errorMessage = xhr.response || 'Unable to upload file';
	        // Upload failed. Do something here with the error.
	        
          uploadInterrupt("Upload failed"+errorMessage);
	    }
	};
  xhr.onerror = function()
  {
    
    //alert('Unable to upload, please check your connections');
    uploadInterrupt('Unable to upload, please check your connections');
  };
	xhr.open('POST', 'https://content.dropboxapi.com/2/files/upload');
	xhr.setRequestHeader('Authorization', 'Bearer ' + uploadDXXX['xxdd']);

	xhr.setRequestHeader('Content-Type', 'application/octet-stream');
	var params = JSON.stringify({
      path: uploadPath+  getUploadFileName(file.name),
      mode: 'overwrite',
      autorename: false,
      mute: false
  });
  console.log("Upload via http"+params);
  xhr.setRequestHeader('Dropbox-API-Arg',(params));

	xhr.send(file);
  }

  

function displayInitUploadBusyDialog()
{
  
  document.getElementById('busy_dialog').style.display="block";
  document.getElementById("busy_dialog_header").style.display = "none";

  document.getElementById("init_upload_busy_dialg_div").style.display = "block"; 
  
}

function dismissInitBusyDialog()
{
  document.getElementById("init_upload_busy_dialg_div").style.display = "none"; 

  //$('#busy_dialog').modal('toggle');
}

function dismissBusyDialog()
{
  document.getElementById('busy_dialog').style.display = "none";
  
}

function displayInitFileUploadBusyDiag()
{
  var progressBusyDilagParent = document.getElementById("init_file_upload_busy_dialg_div");
  
   if (progressBusyDilagParent.style.display === "none") {
    progressBusyDilagParent.style.display = "block";
    }

}

function dismissInitFileUploadBusyDiag()
{
  var progressBusyDilagParent = document.getElementById("init_file_upload_busy_dialg_div");
  
   if (progressBusyDilagParent.style.display === "block") {
    progressBusyDilagParent.style.display = "none";
    }
}

function checkAndDisplayBusyModel()
{
  var busyDialog = document.getElementById('busy_dialog');
  if(busyDialog.style.display=="block")
  {
    
  }else
  {
    
    busyDialog.style.display = "block";
  }
}

function initUploadFileBusyDialg()
{
   checkAndDisplayBusyModel();
   
   displayInitFileUploadBusyDiag();
   /**/
  
  //set uploading file info
  setUploadingFileInfo();

   var progressBusyDilagParent = document.getElementById("file_upload_progress_dialg_parent_div");
  
   if (progressBusyDilagParent.style.display === "block") {
    progressBusyDilagParent.style.display = "none";
    }

    //update the progress,, reset to zero
 
   var progressBusyDilag = document.getElementById("file_upload_progress_dialg_div");
    progressBusyDilag.style.width = 0 + '%'; 
    progressBusyDilag.innerHTML = 0 * 1  + '%';

}

function setUploadingFileInfo()
{
  var uploadingFileInfoDiv = document.getElementById("uploading_file_info_div");
  
   if (uploadingFileInfoDiv.style.display === "none") {
    uploadingFileInfoDiv.style.display = "block";
    }
    
    
    //document.getElementById("uploading_file_name_elm").innerHTML = uploadFiles[uploadingFilePos].name;
    document.getElementById("uploading_file_name_elm").innerHTML = "Uploading Campaign ("+campaignName+")";
    document.getElementById("uploading_file_count_elm").innerHTML=(uploadingFilePos+1)+"/"+uploadFiles.length;

}

function updateFileProgressBusyDialog(progress, updatedBytes = null)
{
  //$("#busy_dialog").modal();

 /*var initBusyDilag = document.getElementById("init_file_upload_busy_dialg_div");
  if (initBusyDilag.style.display === "block") {
    initBusyDilag.style.display = "none";
    } */
  
  var progressBusyDilagParent = document.getElementById("file_upload_progress_dialg_parent_div");
   if (progressBusyDilagParent.style.display === "none") {
    progressBusyDilagParent.style.display = "block";
    }

    //update the progress
 var progressBusyDilag = document.getElementById("file_upload_progress_dialg_div");

    progressBusyDilag.style.width = progress + '%';
    if(updatedBytes== null)
    {
      progressBusyDilag.innerHTML = progress * 1  + '%';
    }else
    {
      progressBusyDilag.innerHTML = ""+updatedBytes;
    } 
    

    
}

function initUpload()
{
  if(info!=null && campaignInfoFile!=null)
  {
    
    displayInitUploadBusyDialog();
   
   if(uploadDXXX!=null && Object.keys(uploadDXXX).length>=1)
    {

    var xhr = new XMLHttpRequest();
    var params = 'accessToken=web&info='+info+'&campaign='+campaignName+'&size='+size;
    
    xhr.onload = function() {
        if (xhr.status === 200) {
            var responseObj = JSON.parse(xhr.response);
            // Upload succeeded. Do something here with the file info.
            dismissInitBusyDialog();

            if(responseObj.statusCode == 0)
            {
               uploadPath = responseObj.save_path;
               
               uploadFile(uploadFiles[0]);
            }else
            {
              dismissBusyDialog();
              alert(responseObj.status);
            }
            
        }
        else {
            var errorMessage = xhr.response || 'Unable to upload file';
            // Upload failed. Do something here with the error.
            
            alert("unable to upload - "+errorMessage);
        }
    };

    xhr.open('POST', '/campaigns/init/');
     
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

    xhr.setRequestHeader("X-CSRFToken", csrf_token);
    xhr.send(params);
  }else
   {
         initUploadDxxx();
    }
  }else
  {
    alert("Please select campaign");
  }
  return false;
}

function checkAndUploadNextFile()
{
  ++uploadingFilePos;
  
  if(uploadFiles.length > uploadingFilePos)
  {
    uploadFile(uploadFiles[uploadingFilePos]);
  }else
  {
    dismissBusyDialog();
    alert("Campaign has been uploaded successfully");
    location.reload();
  }
}

function initUploadDBxxFail(warningMsg)
{
  alert(warningMsg);
  dismissBusyDialog();
  location.reload();
}

function uploadInterrupt(warningMsg)
{

   var isConfirm = confirm(warningMsg+"\n"+"\t Would you like to retry?");
  if(isConfirm)
  {
     //retry uploading
     
     retryUpload();
  }else{
    dismissBusyDialog();
    location.reload();
  }
}

function retryUpload()
{
  var uploadingFile = uploadState.file;
  if(uploadingFile==null || uploadingFile == undefined)
  {
   reUploadFile();

  }else if(uploadingFile.size < UPLOAD_FILE_SIZE_LIMIT)
  {
    reUploadFile();
  }else{
     reUploadLargeFileChunks(uploadingFile);
  }
}

function reUploadFile()
{
   
    if(uploadFiles.length > uploadingFilePos)
    {
      uploadFile(uploadFiles[uploadingFilePos]);
    }
}

function reUploadLargeFileChunks(file)
{
  if(uploadState.current_chunk <= 0)
  {
    //upload from begining
    reUploadFile()
  }else if(uploadState.current_chunk == uploadState.total_chunks)
  {
     //upload last chunk of file
     uploadLastChunkOfFile(uploadState.cursor,uploadState.blob);
  }else
  {
    checkAndReUploadchunks(uploadState.session_id,uploadState.file);
  }
}

function checkAndReUploadchunks(sessionId,file)
{
  
  
      var dbx = new Dropbox.Dropbox({ accessToken: uploadDXXX['xxdd'] });

  var workItems = [];     
      
       var offset = 0;
        while (offset < file.size) {
          var chunkSize = Math.min(maxBlob, file.size - offset);
          workItems.push(file.slice(offset, offset + chunkSize));
          offset += chunkSize;
        } 
        
        uploadState.total_chunks = workItems.length;

        const task = workItems.reduce((acc, blob, idx, items) => {

         
          if (idx < items.length-1) {  
            // Append part to the upload session
            if(idx<uploadState.current_chunk)
            {
              return acc;
            }
            else
            {
            return acc.then(function() {
            
            if(idx==1)
            {
              dismissInitFileUploadBusyDiag();
            }

            //update current chunk
            uploadState.current_chunk = idx;

            updatePercentageForlargeFile();

             var cursor = { session_id: sessionId, offset: idx * maxBlob };
            
            
             uploadState.cursor = cursor;

             return dbx.filesUploadSessionAppendV2({ cursor: cursor, close: false, contents: blob }).then(() => sessionId); 

            });
            }
          } else {
            
            // Last chunk of data, close session
            return acc.then(function(sessionId) {
              
              //update current chunk
            uploadState.current_chunk = idx;

            updatePercentageForlargeFile();

              var cursor = { session_id: sessionId, offset: file.size - blob.size };

              uploadState.session_id = sessionId;
              uploadState.cursor = cursor;
              uploadState.blob = blob;

              var commit = { path: uploadPath+getUploadFileName(file.name), mode: 'add', autorename: true, mute: false };              
              return dbx.filesUploadSessionFinish({ cursor: cursor, commit: commit, contents: blob });           
            });
          }          
        }, Promise.resolve());
        
        task.then(function(result) {
         /* var results = document.getElementById('results');
          results.appendChild(document.createTextNode('File uploaded!'));*/

          checkAndUploadNextFile();

        }).catch(function(error) {
          
          //alert("Unable to upload error "+error);
          uploadInterrupt("Unable to upload error "+error);
        });
        
      }


function uploadLastChunkOfFile(cursor,blob)
{
  
      var dbx = new Dropbox.Dropbox({ accessToken: uploadDXXX['xxdd'] });

            
   var commit = { path: uploadPath+getUploadFileName(file.name), mode: 'add', autorename: true, mute: false };    

     dbx.filesUploadSessionFinish({ cursor: cursor, commit: commit, contents: blob })           
          .then(function(response) {
            checkAndUploadNextFile();

        }).catch(function(error) {
          
          //alert("Unable to upload error "+error);
          uploadInterrupt("Unable to upload error "+error);
        });
}

function getUploadFileName(fileName)
{
   if(uploadFilesTempNames !== 'undefined' && 
    uploadFilesTempNames.hasOwnProperty(fileName))
   {
     return (uploadFilesTempNames[fileName]);
   }else
   {
    return (fileName);
   }
}
