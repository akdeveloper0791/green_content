var downloadThumbInfo = {
    id: 0,
    save_path: null,
    resourceName: null,//resource name
    store_location: 2,//default to drop box
    media_type:1,//campaign type
  };

function afterLoad()
{
	
	downloadThumbInfo.save_path = 
	  document.getElementById("file_path").value;
	downloadThumbInfo.resourceName = 
	  document.getElementById("file_name").value;
	downloadThumbInfo.store_location = 
	  document.getElementById("store_location").value;
	 
	  downloadThumbFile();
}

function checkAndDownloadThumbFile()
{
	alert("Unable to preview");
}

function updateThumbPreview(url)
{
	
   //reform url to display preview
   var res = url.split("?");
   url = res[0]+"?raw=1";
   document.getElementById('content_view').src = url;
   //checkAndDownloadThumbFile();
 
}

