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

//get pixels from percentage
 function getPixels(totalPixels,percentage)
 {
 	return Math.round((percentage*totalPixels)/100)+"px";
 }

 function getPercentagePixels(totalPixels,elemPixels)
 {
  var elemPixels = parseInt(elemPixels.replace('px',''));
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
    }else{
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
    childTag.style.width = getPixels(screenInfo['width'],info.width);
    childTag.style.height = getPixels(screenInfo['height'],info.height);
    childTag.onclick=function(){
        	displayRegSelectOption(idPosition);
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
    childTag.style.position="relative";
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
  	
  	node = document.getElementById('reg_div_'+idPosition);
  	while (node.hasChildNodes()) {
    node.removeChild(node.lastChild);
    } 
  }

  function displayRegSelectOption(idPosition)
  {
    regInfo = regionsInfo[idPosition];
    if(regInfo.hasOwnProperty('is_display_table')&& 
      regInfo['is_display_table'] == false)
    {
      document.getElementById('display_create_table_region').style.display="none";
    }else{
      document.getElementById('display_create_table_region').style.display="block";
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
       'isScrollAnim':false,'isBold':document.getElementById('create_txt_media_txt_bold').checked,
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
    childTag.style.width = getPixels(screenInfo['width'],info.width);
    childTag.style.height = getPixels(screenInfo['height'],info.height);
    
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
         childTag.style.width = getPixels(screenInfo['width'],info.width);
         childTag.style.height = getPixels(screenInfo['height'],info.height);
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
  console.log("Inside display create campaign dialog");
  if(Object.keys(regionsResourceFiles).length>=1)
  {
    document.getElementById("file_duration").value = duration;
   document.getElementById('campaign_info_diag').style.display="block";
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
  var mediaName = document.getElementById("file_media_name").value;
  var playDuration = document.getElementById("file_duration").value;
  if((mediaName==null || mediaName.trim()=='') || playDuration<=0 )
  {
    swal("Please enter valid details");
  }else{
    dismissCreateCampaignDialog();
    
    for (key in regionsResourceFiles) {
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
  var playDuration = document.getElementById("file_duration").value;
  var infoJSON = { "type": "multi_region", "regions": regionsInfo,
  "duration": playDuration }; 
  
  info = JSON.stringify(infoJSON);
  //var blob = new Blob([info], {type: "text/plain;charset=utf-8"});
  campaignName = mediaName;
  campaignInfoFile = new File([info], mediaName+".txt");
  
  size += campaignInfoFile.size;
  uploadFiles.push(campaignInfoFile);
 
 displayInitUploadBusyDialog();
   clearParentDiv();
   prepareThumbView(0);
  //clearParentDiv();
  
  //initUpload();
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
      initUpload();
    },'image/jpg', 0.95); 
      ////
  });
   
    
}


function prepareThumbView(i)
{
  if(regionsInfo.length>i)
  {
    var info = regionsInfo[i];
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

function initDraw(canvas) {

    var regPosition=0;
    screenInfo = {'width':640,'height':360};

    function setMousePosition(e) {
        var ev = e || window.event; //Moz || IE
        if (ev.pageX) { //Moz
            mouse.x = (ev.pageX-custom_x);
            mouse.y = (ev.pageY-custom_y);
        } else if (ev.clientX) { //IE
            mouse.x = ev.clientX + 0;
            mouse.y = ev.clientY + 0;
        }
    };

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
    var element = null;

    canvas.onmousemove = function (e) {
       if(isDraw)
       {
        setMousePosition(e);
        if (element !== null) {
            element.style.width = Math.abs(mouse.x - mouse.startX) + 'px';
            element.style.height = Math.abs(mouse.y - mouse.startY) + 'px';
            //console.log("on mouse move - mouse.x"+mouse.x)
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
            console.log("finsihed.width-"+element.style.width+",height.y"+element.style.height);
            console.log("finsihed.left-"+element.style.left+",top.y"+element.style.top);
            
             prepareInfoForCustomDiv(element.style.width,element.style.height,
              element.style.left,element.style.top);
             element = null;
            ++regPosition;
        } else {
            console.log("begun.mouse.x-"+mouse.x+",mouse.y"+mouse.y);
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
        console.log("is draw false");
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
      console.log(getPercentagePixels(screenInfo['width'],widthPx));
      console.log(JSON.stringify(customDivInfo));

      regionsInfo.push(customDivInfo);
      addImgReg(regPosition,null);
    }
}

