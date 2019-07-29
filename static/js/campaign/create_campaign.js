var regionsInfo=[];
var regionsResourceFiles = new Object();
var w = window,
    d = document,
    e = d.documentElement,
    g = d.getElementsByTagName('body')[0],
    x = w.innerWidth || e.clientWidth || g.clientWidth,
    y = w.innerHeight|| e.clientHeight|| g.clientHeight;

var uploadFilesTempNames = new Object();
var screenInfo = {'width':x,'height':(y-50)};//50 pixels for submit button
var duration = 10;//seconds  
var isRssFeed=false;
function updateScreenSize()
{
  var w = window,
    d = document,
    e = d.documentElement,
    g = d.getElementsByTagName('body')[0],
    x = w.innerWidth || e.clientWidth || g.clientWidth,
    y = w.innerHeight|| e.clientHeight|| g.clientHeight;
    screenInfo = {'width':x,'height':(y-50)};//50 pixels for submit button
}
//get pixels from percentage
 function getPixels(totalPixels,percentage)
 {
 	return Math.round((percentage*totalPixels)/100)+"px";
 }

 function getPercentagePixels(totalPixels,elemPixels)
 {
  if(typeof elemPixels == "string")
  {
    var elemPixels = parseInt(elemPixels.replace('px',''));
  }
  
  //var totalPixels = parseInt(totalPixels.replace('px','')); 
  //return (elemPixels*100);
  var floatPercentage = ((100*elemPixels)/totalPixels);
  return Math.round(floatPercentage * 100) / 100
  
 }

 function setInfoTitle(msg)
 {
   var elem = document.getElementById("info_title");
   elem.style.display="block";
   elem.innerHTML=msg;
   
 }

 function displayUpload()
 {
   document.getElementById("create_button").style.display="block";
      document.getElementById("button1").style.display="block";
 }


function prepareView(selectedTemplate)
{
  try{

    displayUpload();
	  
    cctDismissTemplates();
    if(selectedTemplate=="custom")
    {
      setInfoTitle("Start draw your campaigns with mouse");
      constructCustomDiv();
    }else if(selectedTemplate=="ticker_text")
    {
      setInfoTitle("Write your own Ticker text");
      prepareTickerText();
    }else if(selectedTemplate=="rss")
    {
      setInfoTitle("Start draw your RSS Feeds campaigns with mouse");
      isRssFeed=true;
      constructCustomDiv();
    }
    else{
      setInfoTitle("Add Content to Campaign");
      var templateInfo = JSON.parse(selectedTemplate);
      regionsInfo = templateInfo.regions;
      constructDivs();
    }
  	
  }catch(err)
  {

  	swal("Unable to create view"+err.message);
  }
	
	
}

function constructDivs()
{
	for(var i=0;i<regionsInfo.length;i++)
 	{
 		info = regionsInfo[i];
 		var parentDiv = document.createElement('div');
        //parentDiv.class='generic';
        parentDiv.id = 'reg_div_'+i;
        parentDiv.style.position="absolute";
        parentDiv.style.top=getPixels(screenInfo['height'],info.top_margin);
        parentDiv.style.left=getPixels(screenInfo['width'],info.left_margin);
        parentDiv.style.border = "groove #4de4c0";
        parentDiv.style.width = getPixels(screenInfo['width'],info.width);
        parentDiv.style.height = getPixels(screenInfo['height'],info.height)
        //document.getElementsByTagName('body')[0].appendChild(parentDiv);
        document.getElementById('parent_div').appendChild(parentDiv);
        addImgReg(i,null);
        
        
 	}
 }
    
 function addImgReg(idPosition,file)
  {
  	//get region info 
  	info = regionsInfo[idPosition];
  	removeChildElement(idPosition);
    //create child tag
    var childTag = document.createElement('IMG');
  	info.type="Image";
    info.properties = {"scaleType":"fillScreen"};
    childTag.src= '/static/images/campaign/campaign_default2.png';
    info.is_self_path = true; 

    if(file==null)
  	{
  		
  		info.media_name = "default";	
  	}else{
      info.media_name = getUploadMediaName(file.name);
      var reader = new FileReader();    
        reader.onload = function (e) {
          
          childTag.src = e.target.result;
          
          
        };     
        reader.readAsDataURL(file);
    }
  	
    childTag.id='reg_div_child_'+idPosition;
    /*childTag.style.width = getPixels(screenInfo['width'],info.width);
    childTag.style.height = getPixels(screenInfo['height'],info.height);
    childTag.style.position="absolute";*/

    childTag.style.width = '100%';
    childTag.style.height = '100%';
    childTag.style.position="absolute";

    childTag.onclick=function(){
       if(isRssFeed)
            {
              //display rss url dialog
              displayCreateRSSDialog(idPosition);
            }else
            {
              displayRegSelectOption(idPosition);
            }

        };
    document.getElementById('reg_div_'+idPosition).appendChild(childTag);

  	regionsInfo[idPosition] = info;
  }

  function addVideoRegion(idPosition,file)
  {
  	//get region info 
  	info = regionsInfo[idPosition];
  	removeChildElement(idPosition);
    //create child tag
    var childTag = document.createElement('VIDEO');
  	if(file==null)
  	{
  		
  		info.media_name = "default";
  		
  	  childTag.src= '/static/images/campaign/campaign_default2.png';

  	}else{
  		info.media_name = getUploadMediaName(file.name);
  		var fileUrl = window.URL.createObjectURL(file);
  		
      //get duration
      childTag.preload = 'metadata';
      childTag.onloadedmetadata = function() {
      
       var tempDuration = parseInt(childTag.duration);
       
       if(tempDuration>duration)
       {
        duration = tempDuration;
       }
      }
     childTag.src= fileUrl;
  	}
  	childTag.id='reg_div_child_'+idPosition;
    childTag.style.width = '100%';
    childTag.style.height = '100%';
    childTag.style.position="absolute";
    childTag.style.border = "0";
    childTag.scrolling = false;

    childTag.autoplay=true;

    info.properties = {"isStretch":true,"volume":100};
    info.type="Video";
    info.is_self_path = true;
    
    childTag.onclick=function(){
        	displayRegSelectOption(idPosition);
        };
    parentTag = document.getElementById('reg_div_'+idPosition);

    parentTag.style.width = getPixels(screenInfo['width'],info.width);
    parentTag.style.height = getPixels(screenInfo['height'],info.height);

    parentTag.appendChild(childTag);

  	regionsInfo[idPosition] = info;
  }

  function removeChildElement(idPosition)
  {
  	
  	var parentNode = document.getElementById('reg_div_'+idPosition);
  	var childNodes = parentNode.childNodes.length;
    var pos=0;
    while (parentNode.hasChildNodes() && pos<childNodes) {
      
      if(!(parentNode.lastChild.id == 'reg_div_'+idPosition+"_options_div" || 
        parentNode.lastChild.id == 'reg_div_'+idPosition+"_resize_custom_div"))
      {
        
        parentNode.removeChild(parentNode.lastChild);
      }
       pos+=1;
    }
    
    
  }

  function displayRegSelectOption(idPosition)
  {
    regInfo = regionsInfo[idPosition];
    if(regInfo.hasOwnProperty('is_display_table')&& 
      regInfo['is_display_table'] == false)
    {
      document.getElementById('display_create_table_region_div').style.display="none";
    }else{
      document.getElementById('display_create_table_region_div').style.display="block";
    }
  
   if(isMobileBrowser())
   {
     document.getElementById('selectoption_mobile').style.display="block";
   }else{
     document.getElementById('selectoption').style.display="block";
   }
  	
  	document.getElementById('select_media_reg_id').value=idPosition;
  }

  function dismissSelectRegOption()
  {
  	if(isMobileBrowser())
   {
     document.getElementById('selectoption_mobile').style.display="none";
   }else{
     document.getElementById('selectoption').style.display="none";
   }
  }
  function selectImgRegion()
  {
  	document.getElementById('select_img_file_type').click();
  }
  function onSelectImgReg(input)
  {
    
  	if (input.files && input.files[0]) 
  	{
       var selectedFile = input.files[0];
       var idPosition = document.getElementById('select_media_reg_id').value;
       regionsResourceFiles[idPosition] = selectedFile;
       //get the region info
       info = regionsInfo[idPosition];
       if(info.type.toLowerCase()=='image')
       {
        info.media_name = getUploadMediaName(selectedFile.name);
        info.is_self_path = true;
        
        regionsInfo[idPosition] = info;

        var reader = new FileReader();    
        reader.onload = function (e) {
        	childTag = document.getElementById('reg_div_child_'+
        		idPosition);
          childTag.src = e.target.result;
          dismissSelectRegOption();
          
        };     
        reader.readAsDataURL(selectedFile);
       }else{
        addImgReg(idPosition,selectedFile);
       }

        dismissSelectRegOption();
        
        input.value=null;
    }else{
      
    }
      console.log("addImgReg:info:"+JSON.stringify(info));
  }

  function selectVideoRegion()
  {
   document.getElementById('select_video_file_type').click();
  }

  function onSelectVideoReg(input)
  {
  	if (input.files && input.files[0]) 
  	{
  		var idPosition = document.getElementById('select_media_reg_id').value;
  		//get the region info
  		info = regionsInfo[idPosition];

  		var selectedFile = input.files[0];
  		regionsResourceFiles[idPosition] = selectedFile;

  		if(info.type.toLowerCase == 'video')
  		{
         info.media_name = getUploadMediaName(selectedFile.name);
         info.is_self_path = true;
         
         regionsInfo[idPosition] = info;

  			 var fileUrl = window.URL.createObjectURL(selectedFile);
  		    childTag = document.getElementById('reg_div_child_'+
        		idPosition);
         
         //get duration
          childTag.preload = 'metadata';
          childTag.onloadedmetadata = function() {
          
           var tempDuration = parseInt(childTag.duration);
           
           if(tempDuration>duration)
           {
            duration = tempDuration;
           }
          }
         childTag.src= fileUrl;
         childTag.autoplay=true;

  		}else{
  			//add video region
  			addVideoRegion(idPosition,selectedFile);
  		}

  		dismissSelectRegOption();

      input.value=null;
    }
  }

  function displayCreateTextRegion()
  {
    dismissSelectRegOption();
    document.getElementById('create_text_modal').style.display="block";
  }

   function dismissCreateTextRegion()
  {
    
    document.getElementById('create_text_modal').style.display="none";
  }

  function onSelectTxtReg()
  {
    //validate fields
    var mediaName = document.getElementById('create_text_media_name').value;
    
    if(mediaName=='' || mediaName==null)
    {

       swal('Please enter your text');
    }else{
      
       var idPosition = document.getElementById('select_media_reg_id').value;
      regionsResourceFiles[idPosition] = null;//no resource file 
       
       //get the region info
       info = regionsInfo[idPosition];
       info.media_name = mediaName;
       info.is_self_path = true;

       //set properties
       info.properties = {'textBgColor':"#"+document.getElementById('create_txt_media_txt_bg').value,
       'textColor':"#"+document.getElementById('create_txt_media_txt_color').value,
       'textSize':document.getElementById('create_text_media_text_size').value,
       'isScrollAnim':document.getElementById('create_txt_media_scroll_anim').checked,
       'isBold':document.getElementById('create_txt_media_txt_bold').checked,
       'isItalic':document.getElementById('create_txt_media_txt_italic').checked,
       'isUnderLine':document.getElementById('create_txt_media_txt_underline').checked,
       'textAlignment':document.getElementById('create_txt_media_txt_algmt').value};
       
       var childTag=null; 
       var isNew = true;
       if(info.type.toLowerCase == 'text')
       {
         isNew = false;
         childTag = document.getElementById('reg_div_child_'+
            idPosition);
       }else{
        info.type = 'text';
        removeChildElement(idPosition);
        //create new text child tag
         childTag = document.createElement('TEXTAREA');
         childTag.onclick=function(){
          displayRegSelectOption(idPosition);
         };
         document.getElementById('reg_div_'+idPosition).appendChild(childTag);
       }
       //update info
       regionsInfo[idPosition] = info;
       //style text child
       styleTextChild(childTag,isNew,idPosition);

       dismissCreateTextRegion();
    }
  }

  function styleTextChild(childTag,isNew,idPosition)
  {
    var info = regionsInfo[idPosition];
    childTag.id='reg_div_child_'+idPosition;
    /*childTag.style.width = getPixels(screenInfo['width'],info.width);
    childTag.style.height = getPixels(screenInfo['height'],info.height);
    */
    childTag.style.width = '100%';
    childTag.style.height = '100%';
    childTag.style.position="absolute";

    childTag.innerHTML = info.media_name;
    var properties = info.properties;

    childTag.style.color = properties.textColor;
    childTag.style.backgroundColor =properties.textBgColor;
    childTag.style.fontSize = properties.textSize+"px";
    if(properties.isBold)
    {
     childTag.style.fontWeight = "bold";
    }else{
     childTag.style.fontWeight = "normal";
    }

    if(properties.isItalic)
    {
     childTag.style.fontStyle = "italic";
    }else{
     childTag.style.fontStyle = "normal";
    }

    if(properties.isUnderLine)
    {
     childTag.style.textDecoration  = "underline";
    }else{
     childTag.style.textDecoration  = "none";
    }
    
    textAllignMent(childTag,properties.textAlignment);

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

 function displayCreateURLDialog()
 {
   dismissSelectRegOption();
   document.getElementById('create_url_reg_dialog').style.display="block";
 }

 function dimissCreateURLDialog()
 {
   document.getElementById('create_url_reg_dialog').style.display="none";
 }





 function onSelectUrlReg()
  {
    //validate fields
    var mediaName = document.getElementById('create_url_reg_url').value;
    
    if(mediaName=='' || mediaName==null)
    {

       swal('Please enter URL');
    }else{
     
       var idPosition = document.getElementById('select_media_reg_id').value;
      regionsResourceFiles[idPosition] = null;//no resource file 
       
       //get the region info
       info = regionsInfo[idPosition];
       info.media_name = mediaName;
       //set properties
       info.properties = {};
       
       var childTag=null; 
       
       if(info.type.toLowerCase == 'url')
       {
         
         childTag = document.getElementById('reg_div_child_'+
            idPosition);
         childTag.src = mediaName;
       }else{
        info.type = 'url';
        info.is_self_path = true;

        removeChildElement(idPosition);
        //create new text child tag
         childTag = document.createElement('iframe');
         childTag.id='reg_div_child_'+idPosition;
         childTag.style.width = '100%';
         childTag.style.height = '100%';
         childTag.style.position="absolute";
         childTag.src = mediaName;
         childTag.onclick=function(){
          displayRegSelectOption(idPosition);
         };
         document.getElementById('reg_div_'+idPosition).appendChild(childTag);
       }

       
       //x.setAttribute("src", "https://www.w3schools.com/jsref/prop_video_autoplay.asp");
       //update info
       regionsInfo[idPosition] = info;
       
       dimissCreateURLDialog();
    }
  }

 function displayCreateRSSDialog(idPosition)
 {
      document.getElementById('create_rss_reg_dialog').style.display="block";
      document.getElementById('rss_media_reg_id').value=idPosition;
 }

 function dimissCreateRSSDialog()
 {
   document.getElementById('create_rss_reg_dialog').style.display="none";
 }


 function onSelectRssReg()
  {
    //validate fields
    var mediaName = document.getElementById('create_rss_reg_url').value;
    var interval = document.getElementById('refresh_interval').value;

 
   //console.log("rssCategory:"+rssCategory);
    
    if(mediaName=='' || mediaName==null)
    {

       swal('Please enter Feed URL');
    }else if(interval=='' || interval==null)
    {
      swal('Please enter valid duration');
    }
    else{
     
       var idPosition = document.getElementById('rss_media_reg_id').value;
      regionsResourceFiles[idPosition] = null;//no resource file 
       
       //get the region info
       info = regionsInfo[idPosition];
       info.media_name = mediaName;

     
       info.rss_text_color="#000000";
       info.rss_text_size=25;

      if(interval>0)
       {
        info.refresh_interval=interval*60;
       }else
       {
         info.refresh_interval=1*60;
       }
      info.rss_text_color="#"+document.getElementById('rss_feed_text_color').value;
      info.bg_color="#"+document.getElementById('rss_feed_text_bg_color').value;
      info.rss_text_size=document.getElementById('rss_feed_text_size').value;
      
       //set properties
       info.properties = {};
       
       var childTag=null;  
       if(info.type.toLowerCase == 'rss')
       {
         
         childTag = document.getElementById('reg_div_child_'+idPosition);
         childTag.src = mediaName;
       }else{
        info.type = 'rss';
        info.is_self_path = true;

        removeChildElement(idPosition);
        //create new text child tag
         childTag = document.createElement('iframe');
         childTag.id='reg_div_child_'+idPosition;
         childTag.style.width = '100%';
         childTag.style.height = '100%';
         childTag.style.position="absolute";
         childTag.src = mediaName;
    
        // childTag.backgroundColor="green";//transparent
         childTag.onclick=function()
         {
          displayCreateRSSDialog(idPosition);
         };
         document.getElementById('reg_div_'+idPosition).appendChild(childTag);
       }

       
       //x.setAttribute("src", "https://www.w3schools.com/jsref/prop_video_autoplay.asp");
       //update info
       console.log("regionsInfo:"+JSON.stringify(info));
       regionsInfo[idPosition] = info;

       
       dimissCreateRSSDialog();
    }
  }


function displayCreateTableRegion()
{
  dismissSelectRegOption();
  document.getElementById('create_table_reg_dialog').style.display="block";
  
}
function dismissCreateTableRegion()
{
  document.getElementById('create_table_reg_dialog').style.display="none";
}

function onSelectTableReg()
{

  var rows = document.getElementById('create_table_reg_rows').value;
  var coloumns = document.getElementById('create_table_reg_coloumns').value;
  
  if(rows>=1 && coloumns>=1)
  {
    dismissCreateTableRegion();

    var idPosition = document.getElementById('select_media_reg_id').value;
    regionInfo = regionsInfo[idPosition];
    //re prepare the regions info
    var Width=(regionInfo.width/coloumns);
    var Height=(regionInfo.height/rows);
    var leftMargin=0;var rightMargin=0;var topMargin=0;var bottomMargin=0;

    newTableArray = [];

    for (var i = 0; i < coloumns; i++) 
    {

      for (var j = 0; j < rows; j++) 
      {


          leftMargin = regionInfo.left_margin + (Width * i);
          rightMargin = regionInfo.right_margin;
          topMargin = regionInfo.top_margin + (Height * j);
          bottomMargin = regionInfo.bottom_margin;

          json = {"width":Width,"height":Height,"top_margin":topMargin,
          "bottom_margin":bottomMargin,"left_margin":leftMargin,"right_margin":rightMargin,"is_display_table":false};

          newTableArray.push(json);
      }
    }
      
      if (newTableArray.length > 0)
      {
             
        
        regionsInfo.splice(idPosition,1);

        for (var i =0 ;newTableArray.length>i;i++)
        {
          newRegion = newTableArray[i];
          regionsInfo.push(newRegion);
        }

        
          
        
        reconstructDivs();
      }
  }
     
  else{
    swal("Please enter valid rows and coloumns");
  }
}

function clearParentDiv()
{

   
    node = document.getElementById('parent_div');
    while (node.hasChildNodes()) {
    node.removeChild(node.lastChild);
    } 
  
}
function reconstructDivs()
{
  //clear all divs 
  clearParentDiv();
  //clear resource files
  regionsResourceFiles = new Object();
  uploadFilesTempNames = new Object();
  //call construct divs again
  constructDivs();
}

function displayCreateCampaignDialog()
{
  
  if(Object.keys(regionsResourceFiles).length>=1)
  {
    document.getElementById("file_duration").value = duration;
   document.getElementById('campaign_info_diag').style.display="block";
if(isRssFeed)
  {
   document.getElementById("camp_duration").style.display="none";
   
  }
  } else{
    swal("Before proceeding further, please add content to campaign");
  }
}

function dismissCreateCampaignDialog()
{
  document.getElementById('campaign_info_diag').style.display="none";
}

function createCampaign()
{

  //check for resource files
  var mediaName = (document.getElementById("file_media_name").value).trim();
 
  
   var playDuration = document.getElementById("file_duration").value;
  if((mediaName==null || mediaName.trim()=='') || playDuration<=0 )
  {
    swal("Please enter valid details");
  }else{
    dismissCreateCampaignDialog();
    
    for (key in regionsResourceFiles) 
    {
        if (regionsResourceFiles.hasOwnProperty(key))
        {
          var file = regionsResourceFiles[key];
          if(file!=null)
          {
            size += file.size;
            uploadFiles.push(file);
          }
          
        }
     }

     //prepare info file and upload
     prepareInfoFile(mediaName);
  }
    
} 

function setDefaultCampaignName(element)
{
  if(element.checked)
  {
    
    var currentdate = new Date();
           var datetime = currentdate.getDate() + "-"
                + (currentdate.getMonth()+1)  + "-" 
                + currentdate.getFullYear() + "_"  
                + currentdate.getHours() + "-"  
                + currentdate.getMinutes() + "-" 
                + currentdate.getSeconds();
           document.getElementById("file_media_name").value=datetime;

  }else{
     document.getElementById("file_media_name").value="";
  }
}

function initXXX()
{
  var ga = document.createElement("script"); //ga is to remember Google Analytics ;-)
   ga.type = 'text/javascript';
   ga.src = "/static/js/campaign/uploadxxx.js";

   ga.id = 'invisible_init';
   document.body.appendChild(ga);

   var elem = document.getElementById("invisible_init");
   elem.parentNode.removeChild(elem);
}

function prepareInfoFile(mediaName)
{
  //prepare regionsInfo file
  var activeRegions = deleteInActiveDivs();
  
 
  var playDuration = document.getElementById("file_duration").value;
  var infoJSON = { "type": "multi_region", "regions": activeRegions,
  "duration": playDuration,'hide_ticker_txt': document.getElementById("create_txt_media_hide_ticker").checked}; 
  
  if(isRssFeed)
  {
    infoJSON.type="rss";
  }
  info = JSON.stringify(infoJSON);

  //var blob = new Blob([info], {type: "text/plain;charset=utf-8"});
  campaignName = mediaName;
  campaignInfoFile = new File([info], mediaName+".txt");
  
  size += campaignInfoFile.size;
  uploadFiles.push(campaignInfoFile);
   
   //update screen size
   updateScreenSize();
   displayInitUploadBusyDialog();
   clearParentDiv();
   prepareThumbView(0);
  //clearParentDiv();
  
  //initUpload();
}

function deleteInActiveDivs()
{
  var newRegions = [];
  for(var i=0;i<regionsInfo.length;i++)
  {
    var info = regionsInfo[i];
    //if activated save info
    if(!(info.hasOwnProperty("is_active") && 
      info['is_active']==false))
    {
      newRegions.push(info);
    }
  }

   return newRegions;
}

function createThumb()
{
  
  html2canvas(document.getElementById("parent_div")).then(canvas => {
    //clearParentDiv();
    //document.body.appendChild(canvas)
      ////
    canvas.toBlob(function(blob) {
      var thumbFile = new File([blob], "DNDM-THUMB-"+campaignName+".jpg");
      size += thumbFile.size;
      
      uploadFiles.push(thumbFile);
      dismissInitBusyDialog();
      clearParentDiv();
      startUpload();
    },'image/jpg', 0.95); 
      ////
  });
   
    
}

function startUpload()
{
  
  
  if(storeLocation == 2)
  {
   initUpload();
  }else{
    initLocalUpload();
  }
}


function prepareThumbView(i)
{
  if(regionsInfo.length>i)
  {
    var info = regionsInfo[i];
    if(info.hasOwnProperty("is_active") && 
      info["is_active"] == false)
    {
       prepareThumbView(++i);
    }else{
    var file = null;
    var childTag = null;
    var isPrepare = false;
    if(info.type=="Image")
    {
      childTag = document.createElement('IMG');
      
      if(regionsResourceFiles.hasOwnProperty(i) )
      {
        file= regionsResourceFiles[i];
        
        var reader = new FileReader();    
          reader.onload = function (e) {
            
            childTag.src = e.target.result;
            prepareThumbView(++i);
            
          };     
          reader.readAsDataURL(file);
      }
      
    }else if(info.type=="Video")
    {
      if(regionsResourceFiles.hasOwnProperty(i) )
      {
        file= regionsResourceFiles[i];
        var fileUrl = window.URL.createObjectURL(file);
        videoTag = document.createElement('VIDEO');
        //document.getElementById('parent_div').appendChild(videoTag);
        childTag1 = document.createElement("CANVAS");
        childTag = document.createElement("IMG");
        //document.getElementById('parent_div').appendChild(childTag1);
        ctx = childTag1.getContext("2d");
        videoTag.addEventListener("loadedmetadata", function()
         {i = window.setTimeout(function() {
          ctx.drawImage(videoTag,5,5,260,125)
          childTag.src=childTag1.toDataURL();
          
          prepareThumbView(++i);
        },500);}, false);
        
        
        videoTag.src= fileUrl;

        isPrepare = false;
    
      }
    }else if(info.type=="text")
    {
      childTag = document.createElement("TEXTAREA");
      styleTextChild(childTag,false,i);
    }else if(info.type=="URL")
    {
      childTag = document.createElement('iframe');
      childTag.src = info.media_name;
    }
    
    if(childTag!=null)
    {  
      childTag.id=i;  
      childTag.style.width = getPixels(screenInfo['width'],info.width);
      childTag.style.height = getPixels(screenInfo['height'],info.height);
      
      
      //childTag.style.position="fixed";
      childTag.style.top=getPixels(screenInfo['height'],info.top_margin);
      childTag.style.left=getPixels(screenInfo['width'],info.left_margin);
      childTag.style.border = "groove #4de4c0";
      document.getElementById('parent_div').appendChild(childTag);
    }

    if(file==null || isPrepare)
    {
      prepareThumbView(++i);
    }
   }
  }else{
    createThumb();
  }
}

function getUploadMediaName(selectedFileName)
{
  if(selectedFileName.startsWith("DNDM-"))
  {
    tempName = selectedFileName;
  }else{
    //add DNDM
    tempName = "DNDM-"+selectedFileName;
  }

  //save to array
  uploadFilesTempNames[selectedFileName] = tempName;

  return tempName;
}

function constructCustomDiv()
{

     var parentDiv = document.createElement('div');
        //parentDiv.class='generic';
        parentDiv.id = 'custom';
       
        //document.getElementsByTagName('body')[0].appendChild(parentDiv);
        document.getElementById('parent_div').appendChild(parentDiv);
        initDraw(parentDiv);
}

function initDraw(canvas) 
{

    var regPosition=0;
    screenInfo = {'width':800,'height':450};
    
    var element = document.getElementById('custom');
    var position = element.getBoundingClientRect();
    var custom_x = position.left;
    var custom_y = position.top;
   
    var isDraw = true;
    var mouse = {
        x: 0,
        y: 0,
        startX: 0,
        startY: 0
    };

    var resizeMouse = {startX:0,startY:0,re_element:null};


    var element = null;

    function setMousePosition(e) {
        var ev = e || window.event; //Moz || IE
        if (ev.pageX) { //Moz
            mouse.x = (ev.pageX-custom_x);
            mouse.y = (ev.pageY-custom_y);
        } else if (ev.clientX) { //IE
            mouse.x = ev.clientX -custom_x;
            mouse.y = ev.clientY -custom_y;
        }
    };



    canvas.onmousemove = function (e) {
      
       if(isDraw)
       {
        setMousePosition(e);
        if (element !== null) {
            element.style.width = Math.abs(mouse.x - mouse.startX) + 'px';
            element.style.height = Math.abs(mouse.y - mouse.startY) + 'px';
            
            element.style.left = (mouse.x - mouse.startX < 0) ? mouse.x + 'px' : mouse.startX + 'px';
            element.style.top = (mouse.y - mouse.startY < 0) ? mouse.y + 'px' : mouse.startY + 'px';


        }
      }
    }

    canvas.onclick = function (e) {
     if(isDraw)
     {
        
        if (element !== null) {
            
            canvas.style.cursor = "default";            
            
            
              prepareInfoForCustomDiv(element.style.width,element.style.height,
             element.style.left,element.style.top);
 

              //element.style.border = "0";
             addHoverOptions(element);
             

             element = null;
              ++regPosition;
        } else {
            
            mouse.startX = mouse.x;
            mouse.startY = mouse.y;
            element = document.createElement('div');
            element.className = 'rectangle'
            //element.style.border = "groove #4de4c0"
            element.style.left = mouse.x + 'px';
            element.style.top = mouse.y + 'px';
            element.id="reg_div_"+regPosition;
            
          
            element.onclick=function(){
              if(element==null)
              {
                isDraw = false;
                
              }
              
            };

            if(element!=null)
            {
              canvas.appendChild(element)
              canvas.style.cursor = "crosshair";

              
            }
            
        }
      }else{
        
        isDraw = true;
      }
    }

    function prepareInfoForCustomDiv(widthPx,heightPx,leftPx,topPx)
    {
      var customDivInfo = {'width':getPercentagePixels(screenInfo['width'],widthPx),
      'height':getPercentagePixels(screenInfo['height'],heightPx),
      'top_margin':getPercentagePixels(screenInfo['height'],topPx),
      'left_margin':getPercentagePixels(screenInfo['width'],leftPx),
      'right_margin':0,'bottom_margin':0};
      
      regionsInfo.push(customDivInfo);
      addImgReg(regPosition,null);
    }

    function addHoverOptions(element)
    {
      var hoverDiv = document.createElement("div");
     
      hoverDiv.className="custom_region_options";
      hoverDiv.id = element.id+"_options_div";

      var dragButton = document.createElement("button");
      dragButton.innerHTML="Move";
      dragButton.id=element.id+"_move";
      dragButton.style.cursor="move";
      dragButton.onclick=function(){
          //moveDiv(element);
        };
      hoverDiv.appendChild(dragButton);

      //

      //delete option 
      var deleteButton = document.createElement("button");
      deleteButton.innerHTML = "Delete";
      deleteButton.id=element.id+"_delete";
      deleteButton.onclick=function()
      {
        deleteDiv(element);
      }
      

      hoverDiv.appendChild(deleteButton);

      //hoverDiv.style.top=(element.style.top+5);
      //hoverDiv.style.left= (element.style.left+5);
      element.appendChild(hoverDiv);

      moveDiv(element);
      
      //add resize options
      var resizeDiv = document.createElement("div");
      resizeDiv.className = "resize_custom_div";
      resizeDiv.id=element.id+"_resize_custom_div";
      //resizeDiv.style.top=element.style.top;
      //resizeDiv.style.left= element.style.left;
      element.appendChild(resizeDiv);

      element.addEventListener("mouseover", function( event ) {   
       var hoverOptions = document.getElementById(element.id+"_options_div");
       hoverOptions.style.display="block";
         
          //hoverDiv.style.display="block";
       }, false);

      element.addEventListener("mouseout", function( event ) {   
       var hoverOptions = document.getElementById(element.id+"_options_div");
       hoverOptions.style.display="none";
         
          //hoverDiv.style.display="block";
       }, false);

      //resizeDiv.addEventListener('mousedown', function(event){
        //startResizing(event,element)}, false);
      resizeDiv.onmousedown = function(){startResizing(event,element)};
      //resizeDiv.addEventListener('mouseup', function(event){
        //stopResizing(event)}, false);
    }

    function startResizing(event,element)
    {
      console.log("start resizing"+element.id);
      event = event || window.event;
      event.preventDefault();
      resizeMouse.startX = parseInt(element.style.left);
      resizeMouse.startY = parseInt(element.style.top);
      resizeMouse.re_element = element;

      
      document.onmousemove=resize;
      document.onmouseup = stopResize;
      
    }

    function resize(event)
    {
      
      var originalNewX = event.pageX;
      var originalNewY = event.pageY;
      if(originalNewX > custom_x+screenInfo['width'])
      {
        originalNewX = custom_x+screenInfo['width'];
      }

      if(originalNewY > (custom_y+screenInfo['height']))
      {
        originalNewY = (custom_y+screenInfo['height']);
      }

      if((originalNewX>=custom_x && originalNewX <= custom_x+screenInfo['width']))
      {
        resizeMouse.re_element.style.width = Math.abs((originalNewX-custom_x)-resizeMouse.startX) + 'px'; 
        
      }

      if((originalNewY>=custom_y && originalNewY <= (custom_y+screenInfo['height']+1)))
      {
        resizeMouse.re_element.style.height = Math.abs((originalNewY-custom_y)-resizeMouse.startY) + 'px';
      }
    }

    function stopResize(e) {
    //console.log("e"+e.id);
    e = e || window.event;
      e.preventDefault();
    document.onmouseup = null;
    document.onmousemove = null;
    isDraw=false;
     
     //update margins
     var reElement = resizeMouse.re_element;
     updateDimension(reElement,reElement.style.width,reElement.style.height);
     //updateDimension(reElement,reElement.style.width,reElement.style.height);
    //document.removeEventListener('mouseup', stopResizing, false);
   }
   function updateDimension(element,width,height)
   {
     
     var reElemid = element.id;
     var reElemIdPosition = parseInt(reElemid.replace("reg_div_",""));
     var reElemInfo = regionsInfo[reElemIdPosition];
     reElemInfo['width']  = getPercentagePixels(screenInfo['width'],width);
     reElemInfo['height'] = getPercentagePixels(screenInfo['height'],height);
     regionsInfo[reElemIdPosition] = reElemInfo;
     
   }

    function deleteDiv(element)
    {
      var deleteElemid = element.id;
      var deleteElemIdPosition = parseInt(deleteElemid.replace("reg_div_",""));
      var deleteReginfo = regionsInfo[deleteElemIdPosition];
      deleteReginfo['is_active']  = false;
      regionsResourceFiles[deleteElemIdPosition] = null;//no resource file 

      regionsInfo[deleteElemIdPosition] = deleteReginfo;
      element.parentNode.removeChild(element);
      
    }

    function moveDiv(element)
    {
      //alert(element.id);
      dragElement(element);
      document.getElementById(element.id+"_move").
      innerHTML="Hold Here and Move";
    }

  function dragElement(elmnt) {
  var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
  if (document.getElementById(elmnt.id+"_move")) {
    /* if present, the header is where you move the DIV from:*/
    document.getElementById(elmnt.id +"_move").onmousedown = dragMouseDown;
  } else {
    /* otherwise, move the DIV from anywhere inside the DIV:*/
    elmnt.onmousedown = dragMouseDown;
  }

  function dragMouseDown(e) {
    e = e || window.event;
    e.preventDefault();
    // get the mouse cursor position at startup:
    pos3 = e.clientX;
    pos4 = e.clientY;
    document.onmouseup = closeDragElement;
    // call a function whenever the cursor moves:
    document.onmousemove = elementDrag;

  }

  function elementDrag(e) {
    e = e || window.event;
    e.preventDefault();
    canvas.style.cursor ="move";
    // calculate the new cursor position:
    pos1 = pos3 - e.clientX;
    pos2 = pos4 - e.clientY;
    pos3 = e.clientX;
    pos4 = e.clientY;
    // set the element's new position:
    var afterMoveTop = (elmnt.offsetTop - pos2); 
    var afterMoveLeft =  (elmnt.offsetLeft - pos1);
    
    var elementHeight = parseInt(elmnt.style.height);
    var elementWidth = parseInt(elmnt.style.width);
    if(chcekAndMove(afterMoveLeft,afterMoveTop,elementHeight,elementWidth))
    {
       elmnt.style.top =  afterMoveTop + "px";
       elmnt.style.left = afterMoveLeft + "px";
       
       //update options div
      //var optionsDiv = document.getElementById(elmnt.id+"_options_div");
      //optionsDiv.style.top=afterMoveTop + "px";
      //optionsDiv.style.left= afterMoveLeft + "px";

      updateMargins(elmnt,afterMoveTop,afterMoveLeft);
    }
   
 
    
  }

  function closeDragElement() {
    /* stop moving when mouse button is released:*/
    document.onmouseup = null;
    document.onmousemove = null;
    canvas.style.cursor = "default";
    isDraw=false;
  }

  function chcekAndMove(afterMoveLeft,afterMoveTop,
    elementHeight,elementWidth)
  {
    if(afterMoveLeft<0 || afterMoveTop <0)
    {
      return false;
    }else{
      var bottomLimit = screenInfo['height'] - (elementHeight);
      var rightLimit = screenInfo['width'] - (elementWidth);
      if(afterMoveTop<=bottomLimit && afterMoveLeft <= rightLimit)
      {
        return true;
      }else{
        return false;
      }
      
      
    }
    
  }

  //update new margins 
   function updateMargins(element,topPx,leftPx)
   {
     id = element.id;
     idPosition = parseInt(id.replace("reg_div_",""));
     info = regionsInfo[idPosition];
     info['top_margin']  = getPercentagePixels(screenInfo['height'],topPx);
     info['left_margin'] = getPercentagePixels(screenInfo['width'],leftPx);
     regionsInfo[idPosition] = info;
     
   }

  
 }
}

function prepareTickerText()
{

      var customDivInfo = {'width':100,
      'height':100,'top_margin':0,'left_margin':0,
      'right_margin':0,'bottom_margin':0};
      
      regionsInfo.push(customDivInfo);

      var parentDiv = document.createElement('div');
        //parentDiv.class='generic';
        parentDiv.id = 'reg_div_0';
        parentDiv.style.position="absolute";
        parentDiv.style.top=0;
        parentDiv.style.left=0;
        parentDiv.style.border = "groove #4de4c0";
        parentDiv.style.width = screenInfo['width']+"px";
        parentDiv.style.height = screenInfo['height']+"px";
        //document.getElementsByTagName('body')[0].appendChild(parentDiv);
        document.getElementById('parent_div').appendChild(parentDiv);

        addImgReg(0,null);

        displayTickerTextReg();
   
}

function displayTickerTextReg()
{
  document.getElementById('create_ticker_text_modal').style.display="block";

}

function dismissCreateTickerTextRegion()
{
  document.getElementById('create_ticker_text_modal').style.display="none";
}

function onSelectTickerTxtReg()
{
    //validate fields
    var mediaName = document.getElementById('create_ticker_text_media_name').value;
    
    if(mediaName=='' || mediaName==null)
    {
       swal('Please enter your text');
    }else{
      
       var idPosition = 0;
       regionsResourceFiles[idPosition] = null;//no resource file 
       
       //get the region info
       info = regionsInfo[idPosition];
       info.media_name = mediaName;
       info.is_self_path = true;

       //set properties
       info.properties = {'textBgColor':"#"+document.getElementById('create_ticker_txt_media_txt_bg').value,
       'textColor':"#"+document.getElementById('create_ticker_txt_media_txt_color').value,
       'textSize':20,
       'isScrollAnim':true,
       'isBold':document.getElementById('create_ticker_txt_media_txt_bold').checked,
       'isItalic':document.getElementById('create_ticker_txt_media_txt_italic').checked
       };

       
       
       var childTag=null; 
       var isNew = true;
       if(info.type.toLowerCase == 'text')
       {
         isNew = false;
         childTag = document.getElementById('reg_div_child_'+
            idPosition);
       }else{
        info.type = 'text';
        removeChildElement(idPosition);
        //create new text child tag
         childTag = document.createElement('TEXTAREA');
         childTag.onclick=null;
         document.getElementById('reg_div_'+idPosition).appendChild(childTag);
       }
       //update info
       regionsInfo[idPosition] = info;
       //style text child
       styleTextChild(childTag,isNew,idPosition);

       dismissCreateTickerTextRegion();

       prepareInfoFile("DNDM_SS_TICKER_TXT");
    }
  }

  function selectPdfRegion()
  {
   document.getElementById('select_pdf_file_type').click();
  }

function onSelectPDFReg(input)
{
   if (input.files && input.files[0]) 
    {
       var selectedFile = input.files[0];
       var idPosition = document.getElementById('select_media_reg_id').value;
       regionsResourceFiles[idPosition] = selectedFile;
       //get the region info
       info = regionsInfo[idPosition];
       if(info.type.toLowerCase()=='file')
       {
        info.media_name = getUploadMediaName(selectedFile.name);
        info.is_self_path = true;
        
        regionsInfo[idPosition] = info;

        var reader = new FileReader();    
        reader.onload = function (e) {
          childTag = document.getElementById('reg_div_child_'+
            idPosition);
          childTag.src = e.target.result;
          dismissSelectRegOption();
          
        };     
        reader.readAsDataURL(selectedFile);
       }else{
        addPdfRegion(idPosition,selectedFile);
       }

        dismissSelectRegOption();
        
        input.value=null;
    }else{
      
    }
// console.log("onSelectPDFReg:info:"+JSON.stringify(info));
}

function addPdfRegion(idPosition,file)
  {
   //get region info 
    info = regionsInfo[idPosition];
    removeChildElement(idPosition);
    //create child tag
    var childTag = document.createElement('FILE');
    info.type="File";
    //info.properties = {"scaleType":"fillScreen"};

      //set properties
       info.properties = {
       'isFitToScreen':true,
       'zoomLevel':1.0,
       'scrollingSpeed':10
       };

    childTag.src= '/static/images/campaign/campaign_default2.png';
    info.is_self_path = true; 

    if(file==null)
    { 
      info.media_name = "default";  
    }else{
      info.media_name = getUploadMediaName(file.name);
      var reader = new FileReader();    
        reader.onload = function (e) {
          
          childTag.src = e.target.result;
          childTag.style.textAlign="center";
          childTag.innerHTML = file.name;
          
          
        };     
        reader.readAsDataURL(file);

    }
    
    childTag.id='reg_div_child_'+idPosition;
    /*childTag.style.width = getPixels(screenInfo['width'],info.width);
    childTag.style.height = getPixels(screenInfo['height'],info.height);
    childTag.style.position="absolute";*/

    childTag.style.width = '100%';
    childTag.style.height = '100%';
    childTag.style.position="absolute";

    childTag.onclick=function(){
              displayRegSelectOption(idPosition);

        };

     document.getElementById('reg_div_'+idPosition).appendChild(childTag);
     filePropertiesDialog();

     console.log("addPdfRegion:info:"+JSON.stringify(info));

    regionsInfo[idPosition] = info;
  }

  function dismissPdfPropertiesDialog()
  {
  document.getElementById('file_properties_diag').style.display="none";
  }

  function filePropertiesDialog()
  {
    document.getElementById('file_properties_diag').style.display="block";
  }

  function setFileProperties()
  {
    var idPosition = document.getElementById('select_media_reg_id').value;
       //get the region info
       info = regionsInfo[idPosition];

       //set properties
       info.properties = {
       'isFitToScreen':document.getElementById('fit_to_screen').checked,
       'zoomLevel':parseFloat(document.getElementById('zoom_level').value),
       'scrollingSpeed':parseInt(document.getElementById('scrolling_speed').value)
       };
       dismissPdfPropertiesDialog();
      //console.log("setFileProperties:info:"+JSON.stringify(info));
  }

