var uploadDXXX = [];
var isFileType=[];

function initUploadDxxx()
  {
    var xhr = new XMLHttpRequest();
    

    xhr.onload = function() {
      
        if (xhr.status === 200) {
            uploadDXXX = JSON.parse(xhr.response);
            
            checkForCampaignInDB();
        }
        else {
          var errorMessage = xhr.response || 'Unable to upload file';
            
            initUploadDBxxFail("Upload failed"+errorMessage);
        }
    };
    xhr.onerror = function()
    {
      
      //alert('Unable to upload, please check your connections');
      initUploadDBxxFail('Unable to preview, please check your connections');
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
}


function checkForCampaignInLocal()
{
   var http = new XMLHttpRequest();
   var campaignUrl = "/media"+savePath+campaignName+".txt"
    http.open('HEAD', campaignUrl, false);
    http.send();
 
    if(http.status == 200)
    {
      constructDivs();
    }else{
      swal("Campaign file not found");
    }
}

function checkForCampaignInDB()
 {
   var xhr = new XMLHttpRequest();
  	xhr.onload = function() {
      if (xhr.status === 200) {
         
          var fileInfo = JSON.parse(xhr.response);
          // Upload succeeded. Do something here with the file info.
          
          constructDivs();
          
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
                swal("No campaign files found");

              }else{
                swal('Unable to display previews please try again later -'+errorMessage);
              }
            }catch(exception)
            {
              swal('Unable to display preview, please try again later -'+errorMessage);
            }
            
            
          }else{
            swal('Unable to display preview');
          }
         
          
         // uploadInterrupt("Upload failed"+errorMessage);
      }
  };
  xhr.onerror = function()
  {
    
    swal('please check your connections');
   
  };
	xhr.open('POST', 'https://api.dropboxapi.com/2/files/get_metadata');
	
	xhr.setRequestHeader('Authorization', 'Bearer ' + uploadDXXX['xxdd']);

	xhr.setRequestHeader('Content-Type', 'application/json');

	
	var params = JSON.stringify({"path":savePath+campaignName+".txt",
    "include_media_info": false,
    "include_deleted": false,
    "include_has_explicit_shared_members": false})
 

	xhr.send(params);
 }

 function constructDivs()
 {
   var hasVideo = false;
 	for(var i=0;i<regionsInfo.length;i++)
 	{
 		info = regionsInfo[i];
 		var parentDiv = document.createElement('div');
        parentDiv.id = 'reg_div_'+i;
        parentDiv.style.position="fixed";
        parentDiv.style.top=getPixels(screenInfo['height'],info.top_margin);
        parentDiv.style.left=getPixels(screenInfo['width'],info.left_margin);
        parentDiv.style.border = "groove #4de4c0";
        document.getElementsByTagName('body')[0].appendChild(parentDiv);
        
        var childTag = null;
        //check and add child div's
        if(info.type.toLowerCase()=='image')
        {
        	childTag = document.createElement('IMG');
        	
        	if(info.media_name!=null && 
        		info.media_name.toLowerCase != 'default')
        	{
        		resource = {};
        		resource[i]=info.media_name;

        		downloadResources.push(resource);

        		childBusyTag = document.createElement('IMG');
                childBusyTag.id="reg_div_busy_child_"+i;
        		childBusyTag.src = '/static/images/ajax-loader.gif';

        		parentDiv.appendChild(childBusyTag);
        		
        	}
        	
        }else if(info.type.toLowerCase()=="video")
        {
           hasVideo=true;
           childTag = document.createElement('iframe');
           childTag.allowfullscreen = true;
           if(info.media_name!=null && 
        		info.media_name.toLowerCase != 'default')
        	{
        		resource = {};
        		resource[i]=info.media_name;
        		
        		downloadResources.push(resource);

        		childTag.src = '/static/images/ajax-loader.gif';
        	}
 
        }else if(info.type.toLowerCase()=="url")
        {
        	childTag = document.createElement('iframe');
        	childTag.src=info.media_name;
        }else if(info.type.toLowerCase()=="text")
        {
        	childTag = document.createElement('div');
        	mediaName=info.media_name;
        	var properties = info.properties;
        	parentDiv.style.backgroundColor =properties.textBgColor;
        	childTag.style.color=properties.textColor;
        	childTag.style.fontSize = properties.textSize+"px";
          if(properties.isBold==true)
        	{
        		childTag.style.fontWeight = 'bold';
        	}
        	if(properties.isItalic == true)
        	{
        		childTag.style.fontStyle = "italic";
        	}
        	if(properties.isUnderLine == true)
        	{
        		childTag.style.textDecoration = "underline";
        	}
            
            textAllignMent(childTag,properties.textAlignment);
            
        	childTag.innerHTML= mediaName;

        	
        }else if(info.type.toLowerCase()=='file')
        {
         var tagId='reg_div_child_'+i;
            isFileType.push(tagId);
           
           childTag = document.createElement('object');
          //childTag = document.createElement('FILE');
          
          if(info.media_name!=null && 
            info.media_name.toLowerCase != 'default')
          {


             //childTag.style.href = info.media_name;
             //childTag.style.target = '_blank';

             resource = {};
            resource[i]=info.media_name;

            downloadResources.push(resource);

            childBusyTag = document.createElement('FILE');
                childBusyTag.id="reg_div_busy_child_"+i;
            childBusyTag.src = '/static/images/ajax-loader.gif';

            parentDiv.appendChild(childBusyTag);
            
          }
          
        }else if(info.type.toLowerCase()=="excel")
        {
          childTag = document.createElement('div');
          mediaName=info.media_name;

          childTag.style.textAlign="center"; 
          childTag.innerHTML= mediaName;
    
        }


        if(childTag!=null)
        {
           childTag.id='reg_div_child_'+i;
           parentDiv.style.width = getPixels(screenInfo['width'],info.width);
           parentDiv.style.height = getPixels(screenInfo['height'],info.height);
          
           childTag.style.width = "100%";
           childTag.style.height = "100%";

            parentDiv.appendChild(childTag);
          
        }

        
 	}
  
  if(regionsInfo.length==1 && hasVideo)
  {
     if(childTag!=null)
     {
       
       document.onkeydown = function(){fullscreen(childTag)};
       swal("Prese \"Down\" key to go to full screen");
     }

     
  }
    
    
 	 checkAndDownloadResourceFile();
 }

 function textAllignMent(textUi,allignMent)
 {
 	if(allignMent==3)
 	{
      textUi.style.textAlign="LEFT"; 
 	}else if(allignMent==5)
 	{
      textUi.style.textAlign="RIGHT";
 	}
 	else if(allignMent==17)
 	{
      textUi.style.textAlign="center";
 	}
 	else if(allignMent==48)
 	{
      textUi.style.textAlign="TOP";
 	}
 	else if(allignMent==80)
 	{
      textUi.style.textAlign="BOTTOM";
 	}
 	else if(allignMent==1)
 	{
      textUi.style.textAlign="CENTER_HORIZONTAL";
 	}
 	else if(allignMent==16)
 	{
      textUi.style.textAlign="CENTER_VERTICAL";
 	}
 }

 //get pixels from percentage
 function getPixels(totalPixels,percentage)
 {
 	return Math.round((percentage*totalPixels)/100)+"px";
 }

 function checkAndDownloadResourceFile()
 {
 	var length = downloadResources.length;
 	
 	if(length>=1)
 	{
 		resource = downloadResources[0];

 		for (var key in resource) {
          resourceId = key;
          break;
        }
        var resourceFile = resource[resourceId];
        
        downloadResoruceFile(resourceId,resourceFile)

 	}
 }

 function downloadResoruceFile(resourceId,resourceFile)
 {
  
 	if(storeLocation==1)
  {
     var resourceurl = "/media"+savePath+resourceFile;
     updateChildPreview(resourceId,resourceurl);
  }else //drop box
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
              updateChildPreview(resourceId,url);
            }else{
              
              
              generateNewLink(resourceId,resourceFile);
            }
          }catch(exception)
          {
      childPreviewError(resourceId,'Unable to display preview, please try again later -'+exception.message);
     }
          
      }
      else {
          var errorMessage = xhr.response;
           
                childPreviewError(resourceId,'Unable to display preview-'+errorMessage);
         
          }
  };
  xhr.onerror = function()
  {
    
    
   childPreviewError(resourceId,'No internet');
  };
  xhr.open('POST', 'https://api.dropboxapi.com/2/sharing/list_shared_links');
  
  xhr.setRequestHeader('Authorization', 'Bearer ' + uploadDXXX['xxdd']);

  xhr.setRequestHeader('Content-Type', 'application/json');

  
  var params = JSON.stringify({"path":savePath+resourceFile,
    })
   
     

  xhr.send(params);
  }

  
 }

 function childPreviewError(resourceId,errorMsg)
 {
 	dismissChildBusy(resourceId);
  
 	var childDiv = document.getElementById('reg_div_child_'+resourceId);
 	var parentDiv = childDiv.parentElement;
 	//create error tag
 	var errorTag = document.createElement('p');
 	errorTag.style.width = childDiv.style.width;
    errorTag.style.height = childDiv.style.height;
    //childDiv.style.display = "none";
    //errorTag.innerHTML = errorMsg;
    parentDiv.appendChild(errorTag);

    //download next resource
    downloadNextResource();

 }

 function downloadNextResource()
 {
 	downloadResources.splice(0,1);
 	checkAndDownloadResourceFile();
 }

 function updateChildPreview(resourceId,url)
 { 
 	dismissChildBusy(resourceId);

 	//reform url to display preview
  if(storeLocation==2)
  {
      var res = url.split("?");
      url = res[0]+"?raw=1";
  }
 
 	
 	var childDiv = document.getElementById('reg_div_child_'+resourceId);
  var tagId='reg_div_child_'+resourceId;

  if(isFileType.includes(tagId))
  {
    if(storeLocation==2)
    {
     childDiv.data = url;
    }else
    {
       //isFileType=false;
      var originName=location.origin;
      //console.log("updateChildPreview originName:"+originName);
      childDiv.data =originName+url;
     //childDiv.style.target = '_blank';
    }
    
  }else
  {
    childDiv.src=url;
  }

 	downloadNextResource();
 }

 //generate new link
 function generateNewLink(resourceId,resourceFile)
 {
 	

   var xhr = new XMLHttpRequest();
  	xhr.onload = function() {
      if (xhr.status === 200) {
         
        var fileInfo = JSON.parse(xhr.response);
        

          try
          {
            var url = fileInfo.url;
            
            updateChildPreview(resourceId,url);
            
          }catch(exception)
          {
			childPreviewError(resourceId,'Unable to display preview, please try again later -'+errorMessage);
		 }
          
      }
      else {
          var errorMessage = xhr.response;
           
                childPreviewError(resourceId,'Unable to display preview-'+errorMessage);
         
          }
  };
  xhr.onerror = function()
  {
    
    
   childPreviewError(resourceId,'No internet');
  };
	
	xhr.open('POST', 'https://api.dropboxapi.com/2/sharing/create_shared_link_with_settings');
	
	xhr.setRequestHeader('Authorization', 'Bearer ' + uploadDXXX['xxdd']);

	xhr.setRequestHeader('Content-Type', 'application/json');

	
	var params = JSON.stringify({"path":savePath+resourceFile,
		 "settings": {
        "requested_visibility": "public"
         }
    });
   
	xhr.send(params);
 }

 function dismissChildBusy(resourceId)
 {
 	try
 	{
 		document.getElementById("reg_div_busy_child_"+resourceId).
 	  style.display="none";
 	}catch(exception)
 	{

 	}
 	
 }