
var campaignsList=[];
var playersList=[];
var selectedPlayers = [];
var isPlayersShowing=false;
var isCampaignsShowing = false;
var selectedCampaigns = [];

function onSelectDevice()
{
  showRuleCreationBtn();
  displayDeviceClassifiers();
}

function showRuleCreationBtn() 
 {
	var creation_btn = document.getElementById("create_btn");
	var deviceId=document.getElementById("dev_id");
    if(deviceId.value=="0")
    {
     creation_btn.style.display = "none";  
     dismissRuleCreation();
    }
    else{
    creation_btn.style.display = "block";
	  dismissRuleCreation();
         
    }

}

function dismissRuleCreation()
{
  document.getElementById("submit_btn").style.display="none";
  document.getElementById("rules_form").style.display="none";
}

function displayRulesCreationForm()
{
	var creation_btn = document.getElementById("create_btn");
	var submit_btn=document.getElementById("submit_btn");

	creation_btn.style.display ="none";
	submit_btn.style.display="block";
	document.getElementById("rules_form").style.display="block";
  hideClassifiers();

    

}


//to get the campaigns list
function getCampaignsFromServer()
  {
    try {
       
    $.ajax(
    {

      type:'POST',
      url: '/campaigns/list_my_campaigns/',
      headers: {            
            'X-CSRFToken': csrf_token
        },
      data:{
                secretKey: 'web',
                
      },
      
      success: function(data)
       {
        
        if(data['statusCode']==0)
        {
        	campaignsList=data['campaigns'];
             
          displayCampaigns();
           
        }
       else
       {

             swal(data['status']);
                                 
       }

    
       },
    
     error: function (jqXHR, exception) {
      console.log(jqXHR.responseText);

      swal(exception+jqXHR.responseText);
     }

    });
    }
      catch(Exception)
      {
        swal(Exception.message);
        }
  }

//to get the players list
 function getPlayersFromServer()
  {
    try {
       
    $.ajax(
    {

      type:'POST',
      url: '/player/getPlayers/',
      headers: {            
            'X-CSRFToken':csrf_token
        },
      data:{
                accessToken: 'web',
                
      },
     
      success: function(data)
       {
        
        if(data['statusCode']==0)
        {
          console.log(JSON.stringify(data));   
          playersList = data.players;
          displayPlayers()
           
        }
       else
       {

             swal(data['status']);
                                 
       }

    
       },
    
     error: function (jqXHR, exception) {
      console.log(jqXHR.responseText);

      swal(exception+jqXHR.responseText);
     }

    });
    }
      catch(Exception)
      {
        swal(Exception.message);
        }
  }

  function displayCampaigns()
  {
    for (var i = 0; i < campaignsList.length; i++) 
    {
      var table = document.getElementById('campaign_list');
      for (var i = 0; i < campaignsList.length; i++) 
      {   var campaign = campaignsList[i];
          var row = table.insertRow(-1);
          var cell = row.insertCell(-1);
          cell.innerHTML = "<input type='checkbox' value="+campaign.id+
          " onclick='handleCampaignSelectEvent(this)'>"+campaign.campaign_name
      }
    }
    
  }

  function displayPlayers()
  {
  	 var table = document.getElementById('player_list');
  		for (var i = 0; i < playersList.length; i++) 
      {   var player = playersList[i];
          var row = table.insertRow(-1);
          var cell = row.insertCell(-1);
          cell.innerHTML = "<input type='checkbox' value="+player.id+
          " onclick='handlePlayerSelectEvent(this)'>"+player.name
      }
  	
}
function dismissSelectPlayerList()
{
  document.getElementById('player_list').style.display="none";
    isPlayersShowing=false;
}
function toggleDisplayPlayers()
{
  if(isPlayersShowing)
  {
    dismissSelectPlayerList();
  }else
  {
    dismissSelectCampaignList();
    document.getElementById('player_list').style.display="block";
     isPlayersShowing=true; 
     if(playersList.length>=1)
     {
       displayPlayers();
     }else
     {
       getPlayersFromServer();
     }
  }
}

function handlePlayerSelectEvent(checkBox)
{
  if(checkBox.checked)
  {
     selectedPlayers.push(checkBox.value)
  }else
  {
    var index = selectedPlayers.indexOf(checkBox.value);
    if(index>=0)
    {
      selectedPlayers.splice(index,1);
    }
  }
  console.log(JSON.stringify(selectedPlayers));
}

function dismissSelectCampaignList()
{
  document.getElementById('campaign_list').style.display="none";
    isCampaignsShowing=false;
}

function toggleDisplayCampaigns()
{
  if(isCampaignsShowing)
  {
    dismissSelectCampaignList();
  }else
  {
    dismissSelectPlayerList();
    document.getElementById('campaign_list').style.display="block";
     isCampaignsShowing=true; 
     if(campaignsList.length>=1)
     {
       displayCampaigns();
     }else
     {
       getCampaignsFromServer();
     }
  }
}

function handleCampaignSelectEvent(checkBox)
{
   if(checkBox.checked)
  {
     selectedCampaigns.push(checkBox.value)
  }else
  {
    var index = selectedCampaigns.indexOf(checkBox.value);
    if(index>=0)
    {
      selectedCampaigns.splice(index,1);
    }
  }
  console.log(JSON.stringify(selectedCampaigns));
}

function createRule()
{
  //validations 
  var deviceKey = document.getElementById("dev_id").value;
  if(deviceKey=="0")
  {
    swal("Please select one device");
    return false;
  }

  var classifier = document.getElementById('classifier_type').value;
  if(classifier=="0")
  {
    swal("Please select one classifier");
    return false;
  }

  var delayDuration = document.getElementById('delay_duration').value;
  if(Number.isInteger(parseInt(delayDuration)) == false)
  {
      delayDuration = 0;
  }

  if(selectedPlayers.length<=0)
  {
    swal("Please select atleast one player");
    return false;
  }

  if(selectedCampaigns.length<=0)
  {
    swal("Please select atleast one campaign");
    return false;
  }

 try {
   ajaxindicatorstart("<img src='/static/images/ajax-loader.gif'><br/> Please wait...!");    
    $.ajax(
    {

      type:'POST',
      url: '/iot_device/createRule',
      headers: {            
            'X-CSRFToken':csrf_token
        },
      data:{
           accessToken: 'web',
           iot_device: deviceKey,
           players:JSON.stringify(selectedPlayers),
           campaigns: JSON.stringify(selectedCampaigns),
           classifier:classifier,
           delay_time:delayDuration,   
      },
     
      success: function(data)
       {
        ajaxindicatorstop();
        if(data['statusCode']==0)
        {
          console.log(JSON.stringify(data));   
          resetFormData();
          dismissCreateRuleForm();
          displayDeviceClassifiers();
           
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

function resetFormData()
{
  playersList=[];selectedPlayers=[];
  campaignsList=[];selectedCampaigns=[];
  document.getElementById('campaign_list').innerHTML="";
  document.getElementById('player_list').innerHTML="";
}

function dismissCreateRuleForm()
{
  document.getElementById('submit_btn').style.display="none";
  document.getElementById('create_btn').style.display="block";
  document.getElementById('rules_form').style.display="none";
}
function resetClassifierList(isVisible=true)
{
  var tableDiv  = document.getElementById("device_classifiers_div");
  document.getElementById("device_classifiers_list").innerHTML = "";
  if(isVisible)
  {
    tableDiv.style.display="block";
  }else
  {
    tableDiv.style.display="none";
  }
  
}
function hideClassifiers()
{
   document.getElementById("device_classifiers_div").style.display="none";
}

function displayDeviceClassifiers()
{
   resetClassifierList();
   var deviceKey = document.getElementById("dev_id").value;
   
   if(deviceKey=="0")
    return false;

    try {
   ajaxindicatorstart("<img src='/static/images/ajax-loader.gif'><br/> Please wait...!");    
    $.ajax(
    {

      type:'POST',
      url: '/iot_device/getCARules',
      headers: {            
            'X-CSRFToken':csrf_token
        },
      data:{
           accessToken: 'web',
           iot_device: deviceKey,
              
      },
     
      success: function(data)
       {
        ajaxindicatorstop();
        if(data['statusCode']==0)
        {
          console.log(JSON.stringify(data));   
          displayClassifiers(data.rules);
           
        }
        else if(data['statusCode']==2)
        {
          displayDeviceClassifiersError(data.status);
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

function displayClassifiers(rules)
{
  var table =document.getElementById("device_classifiers_list");
  for(var i=0;i<rules.length;i++)
  {
    var rule = rules[i];
    var row=table.insertRow(-1);
    row.id="classifier_"+rule.id;
    var cell =row.insertCell(-1);
    cell.innerHTML = rule.classifier;
    cell.style.textAlign = "left"
    cell.style.marginLeft = "100"
    var deleteCell = row.insertCell(-1);
    ///deleteCell.innerHTML = "<i class='fa fa-trash fa-lg' style='color:orangered;cursor: pointer;' alt='Delete' title='Delete' onclick='deleteCampaign("+rule.id+")></i>";
    deleteCell.innerHTML = '<span class="fa fa-trash"  style="cursor:pointer;color:orangered; display:inline-block;width:4%;float: left;margin-left: 01.5%;margin-right: 01.5%; "onclick="deleteRule('+rule.id+')"></span>';
  }
}

function displayDeviceClassifiersError(error)
{
  document.getElementById("device_classifiers_list").innerHTML=error;
}

function deleteRule(ruleId)
{
  try {
   ajaxindicatorstart("<img src='/static/images/ajax-loader.gif'><br/> Please wait...!");    
    $.ajax(
    {

      type:'POST',
      url: '/iot_device/deleteRule',
      headers: {            
            'X-CSRFToken':csrf_token
        },
      data:{
           accessToken: 'web',
           rule_id: ruleId,
              
      },
     
      success: function(data)
       {
        ajaxindicatorstop();
        if(data['statusCode']==0)
        {
          
          deleteRowClassifer(ruleId);
           
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

function deleteRowClassifer(id)
{
    console.log("delete sc row "+id);
    document.getElementById("device_classifiers_list").deleteRow(document.getElementById("classifier_"+id).rowIndex);
}


