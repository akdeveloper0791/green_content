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
console.log("screenInfo"+JSON.stringify(screenInfo));
//get pixels from percentage
 function getPixels(totalPixels,percentage)
 {
 	return Math.round((percentage*totalPixels)/100)+"px";
 }

function prepareView(selectedTemplate)
{
  try{
	  cctDismissTemplates();
    console.log("regionsInfo"+selectedTemplate);
  
  	var templateInfo = JSON.parse(selectedTemplate);
    regionsInfo = templateInfo.regions;
    constructDivs();
  }catch(err)
  {

  	alert("Unable to create view"+err.message);
  }
	
	console.log("regionsInfo"+JSON.stringify(regionsInfo));
}

function constructDivs()
{
	for(var i=0;i<regionsInfo.length;i++)
 	{
 		info = regionsInfo[i];
 		var parentDiv = document.createElement('div');
        parentDiv.class='generic';
        parentDiv.id = 'reg_div_'+i;
        parentDiv.style.position="absolute";
        parentDiv.style.top=getPixels(screenInfo['height'],info.top_margin);
        parentDiv.style.left=getPixels(screenInfo['width'],info.left_margin);
        parentDiv.style.border = "groove #4de4c0";
       
        //document.getElementsByTagName('body')[0].appendChild(parentDiv);
        document.getElementById('parent_div').appendChild(parentDiv);
        addImgReg(i,null);
        /*var childTag = null;
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
        		childBusyTag.src = '{% static "images/ajax-loader.gif" %}';

        		parentDiv.appendChild(childBusyTag);
        		
        	}
        	
        }else if(info.type.toLowerCase()=="video")
        {
           childTag = document.createElement('iframe');

           if(info.media_name!=null && 
        		info.media_name.toLowerCase != 'default')
        	{
        		resource = {};
        		resource[i]=info.media_name;
        		
        		downloadResources.push(resource);

        		childTag.src = '{% static "images/ajax-loader.gif" %}';
        	}

          
        }else if(info.type.toLowerCase()=="url")
        {
        	childTag = document.createElement('iframe');
        	childTag.src=info.media_name;
        }else if(info.type.toLowerCase()=="text")
        {
        	childTag = document.createElement('p');
        	mediaName=info.media_name;
        	var properties = info.properties;
        	parentDiv.style.backgroundColor =properties.textBgColor;
        	childTag.style.color=properties.textColor;
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

        	
        }

        if(childTag!=null)
        {
           childTag.id='reg_div_child_'+i;
           childTag.style.width = getPixels(screenInfo['width'],info.width);
           childTag.style.height = getPixels(screenInfo['height'],info.width);

           parentDiv.appendChild(childTag);
        }*/

        
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
        childTag.src= '/static/images/campaign/campaign_default.png';

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
  		
  	    childTag.src= '/static/images/campaign/campaign_default.png';

  	}else{
  		info.media_name = getUploadMediaName(file.name);
  		var fileUrl = window.URL.createObjectURL(file);
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
  	console.log('reg_div_'+idPosition);
  	node = document.getElementById('reg_div_'+idPosition);
  	while (node.hasChildNodes()) {
    node.removeChild(node.lastChild);
    } 
  }

  function removeParentDiv(idPosition)
  {
    elem = document.getElementById('reg_div_'+idPosition);
    elem.parentNode.removeChild(elem);
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

  	document.getElementById('selectoption').style.display="block";
  	document.getElementById('select_media_reg_id').value=idPosition;
  }

  function dismissSelectRegOption()
  {
  	document.getElementById('selectoption').style.display="none";
  }
  function selectImgRegion()
  {
  	document.getElementById('select_img_file_type').click();
  }
  function onSelectImgReg(input)
  {
    console.log("Inside onSelectImgReg");
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
        console.log("selected file name"+input.files[0].name+", size"+input.files[0].size);
    }else{
      console.log("Unable to select file");
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
         regionsInfo[idPosition] = info;

  			var fileUrl = window.URL.createObjectURL(selectedFile);
  		    childTag = document.getElementById('reg_div_child_'+
        		idPosition);

  		    childTag.src= fileUrl;
          childTag.autoplay=true;

  		}else{
  			//add video region
  			addVideoRegion(idPosition,selectedFile);
  		}

  		dismissSelectRegOption();

       
        console.log("selected file name"+selectedFile.name+", size"+selectedFile.size);
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

       alert('Please enter your text');
    }else{
      console.log(mediaName);
       var idPosition = document.getElementById('select_media_reg_id').value;
      regionsResourceFiles[idPosition] = null;//no resource file 
       
       //get the region info
       info = regionsInfo[idPosition];
       info.media_name = mediaName;
       //set properties
       info.properties = {'textBgColor':document.getElementById('create_txt_media_txt_bg').value,
       'textColor':document.getElementById('create_txt_media_txt_color').value,
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
    info = regionsInfo[idPosition];
    childTag.id='reg_div_child_'+idPosition;
    childTag.style.width = getPixels(screenInfo['width'],info.width);
    childTag.style.height = getPixels(screenInfo['height'],info.height);
    
    childTag.innerHTML = info.media_name;
    var properties = info.properties;

    childTag.style.color = properties.textColor;
    childTag.style.backgroundColor = properties.textBgColor;
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

       alert('Please enter URL');
    }else{
      console.log(mediaName);
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
  console.log("New Regions Before--"+
            JSON.stringify(regionsInfo));
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
             
       

        for (var i =0 ;newTableArray.length>i;i++)
        {
          newRegion = newTableArray[i];
          regionsInfo.push(newRegion);
        }

        //constructTableDiv(idPosition,newTableArray);
          console.log("New Regions--"+
            JSON.stringify(regionsInfo));
        
        reconstructDivs();
      }
  }
     
  else{
    alert("Please enter valid rows and coloumns");
  }
}

function constructTableDiv(idPosition,newTableArray)
{
   //remove tables parent div
   regionsInfo.splice(idPosition,1);
   removeParentDiv(idPosition);
   //delete parent resource
   regionsResourceFiles[idPosition]=null;

  for(var i=0;i<newTableArray.length;i++)
  {
    info = newTableArray[i];
    regionsInfo.push(info);

    var parentDiv = document.createElement('div');
        parentDiv.class='generic';
        parentDiv.id = 'reg_div_'+i;
        parentDiv.style.position="absolute";
        parentDiv.style.top=getPixels(screenInfo['height'],info.top_margin);
        parentDiv.style.left=getPixels(screenInfo['width'],info.left_margin);
        parentDiv.style.border = "thick solid #0000FF";
       
        //document.getElementsByTagName('body')[0].appendChild(parentDiv);
        document.getElementById('parent_div').appendChild(parentDiv);
        addImgReg(i,null);

       
       
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
   document.getElementById('campaign_info_diag').style.display="block";
  } else{
    alert("Nothing selected");
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
    alert("Please enter valid details");
  }else{
    dismissCreateCampaignDialog();
    console.log("regionsResourceFiles"+JSON.stringify(regionsResourceFiles));
    for (key in regionsResourceFiles) {
        if (regionsResourceFiles.hasOwnProperty(key))
        {
          var file = regionsResourceFiles[key];
          if(file!=null)
          {
            size += file.size;
            uploadFiles.push(file);
            console.log("regionsResourceFiles"+file.name+"File size"+file.size);
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
  var infoJSON = { "type": "multi_region", "regions": regionsInfo }; 
  
  info = JSON.stringify(infoJSON);
  //var blob = new Blob([info], {type: "text/plain;charset=utf-8"});
  campaignName = mediaName;
  campaignInfoFile = new File([info], mediaName+".txt");
  console.log(campaignInfoFile.name+"size"+campaignInfoFile.size);
  size += campaignInfoFile.size;
  uploadFiles.push(campaignInfoFile);
  console.log("total upload files"+uploadFiles.length);
  
  clearParentDiv();
  
  initUpload();
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



