var selectedDeviceType=null;
var campaignsList=[];
var playersList=[];
var selectedPlayers = [];
var isPlayersShowing=false;
var isCampaignsShowing = false;
var selectedCampaigns = [];
var carSelectedPlayers=[];
var micClassifierUserList=[];


function onSelectDevice(isDefault = false)
{
   showRuleCreationBtn();
  displayDeviceClassifiers(isDefault);
}

function showRuleCreationBtn() 
 {
	var creation_btn = document.getElementById("create_btn");
	var deviceId=document.getElementById("dev_id");
   
    if(deviceId.value=="1")
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
  if(selectedDeviceType=="Microphone")
  {
    document.getElementById("mic_classifier").style.display="block";
    document.getElementById("mic_classifier_user_list").style.display="block";
    document.getElementById("classifier_type").style.display="none";
    checkAndDisplayMicClassifiers();
  }else
  {
    document.getElementById("mic_classifier").style.display="none";
    document.getElementById("classifier_type").style.display="block";
    document.getElementById("mic_classifier_user_list").style.display="none";
  }
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
      // displayPlayers();
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
      // displayCampaigns();
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

  var classifier = "0";
  if(selectedDeviceType=="Microphone")
  {
    classifier = document.getElementById("mic_classifier").value;
    
    if(classifier=="" || classifier==null)
    {

      swal("Please enter classifier");
      return false;
    }
    classifier = classifier.toLowerCase();
  }else
  {
    classifier = document.getElementById('classifier_type').value;
    if(classifier=="0")
    {
      swal("Please select one classifier");
      return false;
    }
  }
  
  
  var delayDuration = document.getElementById('delay_duration').value;
  if(Number.isInteger(parseInt(delayDuration)) == false)
  {
      delayDuration = 0;
  }

  /*if(selectedPlayers.length<=0)
  {
    swal("Please select atleast one player");
    return false;
  }*/

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

function displayDeviceClassifiers(isDefault = false)
{

   resetClassifierList();
   var deviceKey = document.getElementById("dev_id").value;
   
   if(deviceKey=="0")
    return false;

    try {
      if(isDefault==false)
      {
        ajaxindicatorstart("<img src='/static/images/ajax-loader.gif'><br/> Please wait...!");
      }
       
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
           is_info:true,
              
      },
     
      success: function(data)
       {
         if(isDefault==false)
      {
       ajaxindicatorstop();
      }
      
        setDeviceType(data);
        if(data['statusCode']==0)
        {
          
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
        if(isDefault==false)
      {
       ajaxindicatorstop();
      }
      swal(exception+jqXHR.responseText);
     }

    });
    }
      catch(Exception)
      {
         if(isDefault==false)
      {
       ajaxindicatorstop();
      }
        swal(Exception.message);
      }
}

function setDeviceType(data)
{
  
  if('playerInfo' in data)
  {
     var playerInfo = data['playerInfo'];
     if(playerInfo!=null)
     {
      selectedDeviceType = playerInfo['type'];
     }else
     {
       selectedDeviceType = null;
     }
  }else
  {
    selectedDeviceType = null;
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

//device name
    var deviceName =row.insertCell(-1);
    deviceName.innerHTML =rule.iot_device__name;
  //  deviceName.style.textAlign = "left";

   //device type
    var deviceType =row.insertCell(-1);
    deviceType.innerHTML =rule.iot_device__device_type;
  

  //classifier
    var classifier =row.insertCell(-1);
    classifier.innerHTML =rule.classifier;


             
    var campaignsCell=row.insertCell(-1);
     // campaignsCell.innerHTML="Campaigns";
      campaignsCell.innerHTML='<p style="cursor: pointer;color:blue;"'+
      'onclick="getRuleCampaignInfo('+rule.id+');"><b>Campaign</b></p>'

      /*campaignsCell.style.cursor ="pointer";
      campaignsCell.style.color="blue";
      campaignsCell.onclick=function(){
         getRuleCampaignInfo(rule.id);
        };*/

     var playersCell=row.insertCell(-1);
     playersCell.innerHTML='<p style="cursor: pointer;color:green;"'+
      'onclick="getRulePlayersInfo('+rule.id+');"><b>Players</b></p>'

    var deleteCell = row.insertCell(-1);
    ///deleteCell.innerHTML = "<i class='fa fa-trash fa-lg' style='color:orangered;cursor: pointer;' alt='Delete' title='Delete' onclick='deleteCampaign("+rule.id+")></i>";
    deleteCell.innerHTML = '<span class="fa fa-trash"  style="cursor:pointer;color:orangered; display:inline-block;width:4%;float: left;margin;5px;" onclick="deleteRule('+rule.id+')"></span>';
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

function getRuleCampaignInfo(rule_id)
{
  
  
  try {
        ajaxindicatorstart("<img src='/static/images/ajax-loader.gif'><br/> Please wait...!");
       
    $.ajax(
    {

      type:'POST',
      url: '/iot_device/getCARuleInfo',
      headers: {            
            'X-CSRFToken': csrf_token
        },
      data:{
                accessToken: 'web',
                rule_id: rule_id,
                is_campaigns:true,
                
      },
      
      success: function(data)
       {
         ajaxindicatorstop();
      console.log("data"+JSON.stringify(data));
            
        if(data['statusCode']==0)
        {
        displayRuleCampaignInfo(data,rule_id);       
        }
      else
      {

             swal(data['status']);
                                    
      }

       },
    
     error: function (jqXHR, exception) {
      ajaxindicatorstop();
      alert(exception+jqXHR.responseText);
     }

    });
  }
  catch(Exception)
    {
    alert(Exception.message);
  }

}

function displayRuleCampaignInfo(info,ruleIdValue)
{
     document.getElementById('rule_info').innerHTML=info["rule"] .classifier;
     document.getElementById('rule_campaign_info_id').value=ruleIdValue;
     displayRuleCampaigns(info['campaigns'],ruleIdValue);
     var modal = document.getElementById('rule_campaigns_info');
     modal.style.display = "block";
}

function displayRuleCampaigns(campaigns,ruleId)
{
  var dvTable = document.getElementById("rule_assigned_campaigns");
    
    //init existing campaigns inside Rule
    existedCampaigns=[];

    if(campaigns.length>=1)
    {
        //Create a HTML Table element.
     var table = document.createElement("TABLE");
     table.id="rule_info_campaigns_TABLE";
     table.classList.add("info","table-hover")
     table.border = "0";
     table.style.borderSpacing = "20px";  
     //Get the count of columns.
     // var columnCount = 5;

        
      for (var i = 0; i < campaigns.length; i++) 
      {
         campaign = campaigns[i];

             row = table.insertRow(-1);
             row.id = "campaign_row_"+campaign.campaign__id;
             existedCampaigns.push(campaign.campaign__id);

             {
              var cell = row.insertCell(-1);
              cell.innerHTML =campaign.campaign__campaign_name;

             
              var deleteCell = row.insertCell(-1);
              deleteCell.innerHTML = "<span class='fa fa-trash' alt='Remove' title='Remove' style='cursor:pointer;color:orangered; display:inline-block; margin: 10px;' onclick='removeCampaign("+campaign.campaign__id+")'>"            
             }

         }
  
         dvTable.innerHTML = "";
         dvTable.appendChild(table);
      }else
      {
         //no campaigns
         dvTable.innerHTML = "No campaigns";
      }
}

function displayCampaignsToAdd()
{
   closeRuleCampaignInfo();
    lmcbListCampaigns();   
}

function closeRuleCampaignInfo()
{
  document.getElementById('rule_campaigns_info').style.display="none";
}

function sendLMCBselectedCampaigns()
{
    closeLmcbCampaigns();
   // alert(lmcbselectedCampaigns);
    assignCampaignsApi(lmcbselectedCampaigns);
}

function assignCampaignsApi(campaigns)
{
    
 try {
       ajaxindicatorstart("<img src='/static/images/ajax-loader.gif'><br/> Please wait...!");

    $.ajax(
    {

      type:'POST',
      url: '/iot_device/assignCampaignsToRule',
      headers: {            
            'X-CSRFToken': csrf_token
        },

      data:{
                accessToken: 'web',
                rule_id: document.getElementById('rule_campaign_info_id').value,
                campaigns:JSON.stringify(campaigns)
                
      },
      
      success: function(data)
       {
         ajaxindicatorstop();
       
       console.log("data-"+JSON.stringify(data));
              swal(data['status']);
              if(data['statusCode']==0)
              {
                lmcbselectedCampaigns =[];
                getRuleCampaignInfo(document.getElementById('rule_campaign_info_id').value);
              }
       },
    
     error: function (jqXHR, exception) {
      ajaxindicatorstop();
      alert(exception+jqXHR.responseText);
     }

    });
    }
     catch(Exception)
     {
        ajaxindicatorstop();

        alert(Exception.message);
     }
}


function removeCampaign(campaignId)
{
  
    campaigns = [campaignId];
    
    try {
        ajaxindicatorstart("<img src='/static/images/ajax-loader.gif'><br/> Please wait...!");

    $.ajax(
    {

      type:'POST',
      url: '/iot_device/removeCampaignsFromRule',
      headers: {            
            'X-CSRFToken': csrf_token 
        },

      data:{
                accessToken: 'web',
                //is_campaigns:true,
                rule_id: document.getElementById('rule_campaign_info_id').value,
                campaigns:JSON.stringify(campaigns)
                
      },
      
      success: function(data)
       {
         ajaxindicatorstop();
        
              swal(data['status']);
              if(data['statusCode']==0)
              {
                var table = document.getElementById("rule_info_campaigns_TABLE");

                //after delete ,, check and delete rows
                for(var i=0;i<campaigns.length;i++)
                {
                try
                {
                  var row = document.getElementById("campaign_row_"+campaigns[i]);
                  table.deleteRow(row.rowIndex);

                   //remove from existing campaigns
                var index = existedCampaigns.indexOf(campaigns[i]);
        if (index > -1) {
          existedCampaigns.splice(index, 1);
        }
                }catch(Exception)
                {
                  console.log(Exception.message);
                }
               }
              }

       },
    
     error: function (jqXHR, exception) {
      ajaxindicatorstop();
      alert(exception+jqXHR.responseText);
     }

    });
    }
     catch(Exception)
     {
        ajaxindicatorstop();

        alert(Exception.message);
     }
    
}

//display contextual ad rules assigned player

function getRulePlayersInfo(rule_id)
{
  try {
        ajaxindicatorstart("<img src='/static/images/ajax-loader.gif'><br/> Please wait...!");
       
    $.ajax(
    {

      type:'POST',
      url: '/iot_device/getCARuleInfo',
      headers: {            
            'X-CSRFToken': csrf_token
        },
      data:{
                accessToken: 'web',
                rule_id: rule_id,
                is_devices:true,
                
      },
      
      success: function(data)
       {
         ajaxindicatorstop();
      console.log("data"+JSON.stringify(data));
            
        if(data['statusCode']==0)
        {
        displayRulePlayersInfo(data,rule_id);       
        }
      else
      {
             swal(data['status']);                               
      }

       },
    
     error: function (jqXHR, exception) {
      ajaxindicatorstop();
      alert(exception+jqXHR.responseText);
     }

    });
  }
  catch(Exception)
    {
    alert(Exception.message);
  }
}

function displayRulePlayersInfo(data ,rule_id)
{
  var isPlayersAssigned=false;
  carSelectedPlayers=[];
  console.log("displayRulePlayersInfo:"+JSON.stringify(data));
  document.getElementById('ctad_rule_id').value =rule_id;
  document.getElementById('rule_name').innerHTML=data['rule'].classifier;

  document.getElementById('ctadr_players').style.display="block";
   var dvTable = document.getElementById("ctadr_player_list");

   var players=data['devices']
    console.log("players:"+JSON.stringify(players));
    if(players.length>=0)
    {
            //Create a HTML Table element.
         var table = document.createElement("TABLE");
         table.classList.add("data","table-hover"); 
       
       
        //Add the header row.
       // var row = table.insertRow(-1);

        for (var i = 0; i < players.length; i++) 
        {

          var player = players[i];
          // player_list.push(player.id);
              row = table.insertRow(-1);
             {
              var cell = row.insertCell(-1);

        
             var ruleId = players[i]['car_device_Id'];
              
              if(ruleId>0)
              {
               isPlayersAssigned=true;
                cell.innerHTML = "<input id='ctadr_cb_"+player.id+"' type='checkbox' checked= true disabled= true style='margin:5px;cursor:pointer;' name='name1' onchange='carpOnchange(this,"+player['id']+")'/>";
              }else
              {
                cell.innerHTML = "<input type='checkbox' style='margin:5px;cursor:pointer;'  name='name1' onchange='carpOnchange(this,"+players[i]['id']+")'/>";
              }
              
              var cell = row.insertCell(-1);
              cell.innerHTML = players[i]['name'];

              if(ruleId>0)
              {
                var deleteCell = row.insertCell(-1);
                deleteCell.innerHTML = "<input type='image'style='cursor:pointer;' id='ctadr_unassign_"+player.id+"'src='/static/images/ic_remove.png' alt='remove' title='remove' onclick='carPlayerRemove("+players[i]['id']+")'>"  
              }

             }
        }
    
         dvTable.innerHTML = "";
         dvTable.appendChild(table);

         /*if(!isPlayersAssigned)
         {
          swal("No players assigned to the rule.");
         }*/


    }else
    {
      //no members
      alert("No Players Found");
      //dvTable.innerHTML = "No Players Assigned";
    }

}

//on change lister for players lits checkbox's inside rule
function carpOnchange(element,playerId)
 {
  if(element.checked == true)//check and add player Id to newPlayers List
  {
      if(carSelectedPlayers.includes(playerId)==false)
      {
        carSelectedPlayers.push(playerId);
      }

  }else
  {
    ctadrRemoveSelectedPlayer(playerId)
  }
  
 }

 function ctadrRemoveSelectedPlayer(playerId)
 {
    //if player id is in new players list check and remove it
      var elementIndex = carSelectedPlayers.indexOf(playerId);
       if(elementIndex>=0)
      {
      carSelectedPlayers.splice(elementIndex,1);
      }  
  
 }


 function assignCADRselectedPlayers()
 {
  closeCADRplayers();
  if(carSelectedPlayers.length>=1)
  {
    
    ajaxindicatorstart("<img src='/static/images/ajax-loader.gif'><br/> Please wait...!");
  var xhr = new XMLHttpRequest();
    xhr.onload = function() {
      ajaxindicatorstop();
      if (xhr.status === 200) {
       
        var responseJSON = JSON.parse(xhr.response);
        if(responseJSON['statusCode']==0)
        {
          console.log("newPlayersList:"+JSON.stringify(newPlayersList));
          ///lptpDisplayPlayers(responseJSON['players']);
          swal(responseJSON['status']);
        }else
        {
          swal(responseJSON['status']);
        }
          
      }
      else {
        
          var errorMessage = xhr.response;
           
           swal(errorMessage);
         
          }
  };
  xhr.onerror = function()
  {
    ajaxindicatorstop();
    console.log("Error");
  };
  
  xhr.open('POST', '/iot_device/assignDevicesToRule');
  xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  xhr.setRequestHeader("X-CSRFToken", csrf_token);
  
  
    var params = 'rule_id='+document.getElementById('ctad_rule_id').value+'&players='+JSON.stringify(carSelectedPlayers)+
     '&accessToken=web';
     
    xhr.send(params);
    
  }
   
 }


function carPlayerRemove(playerId)
{
   var players=[];
   players.push(playerId);

  ajaxindicatorstart("<img src='/static/images/ajax-loader.gif'><br/> Please wait...!");
  var xhr = new XMLHttpRequest();
    xhr.onload = function() {
      ajaxindicatorstop();
      if (xhr.status === 200) {
        
        var responseJSON = JSON.parse(xhr.response);
        if(responseJSON['statusCode']==0)
        {
          ctadrRemoveSelectedPlayer(playerId);

          document.getElementById('ctadr_cb_'+playerId).disabled=false;
          document.getElementById('ctadr_cb_'+playerId).checked=false;

          document.getElementById('ctadr_unassign_'+playerId).style.display="none";
        }else
        {
          swal(responseJSON['status']);
        }
          
      }
      else {
        
          var errorMessage = xhr.response;
           
           swal(errorMessage);
         
          }
  };
  xhr.onerror = function()
  {
    ajaxindicatorstop();
    console.log("Error");
  };
  
  xhr.open('POST', '/iot_device/removeDevicesFromRule');
  xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  xhr.setRequestHeader("X-CSRFToken", csrf_token);
  
  console.log("deleteList:"+JSON.stringify(players));
    var params = 'players='+JSON.stringify(players)+'&rule_id='+document.getElementById('ctad_rule_id').value+
     '&accessToken=web';
     
    xhr.send(params);

}



function closeCADRplayers()
{
  document.getElementById('ctadr_players').style.display="none";
  newPlayersList=[];
 
}

function checkAndDisplayMicClassifiers()
{
  console.log("checkAndDisplayMicClassifiers length-"+micClassifierUserList.length)
  if(micClassifierUserList.length<=0)
  {
    //get classifiers
    ajaxindicatorstart("<img src='/static/images/ajax-loader.gif'><br/> Please wait...!");
    var xhr = new XMLHttpRequest();
    xhr.onload = function() {
      ajaxindicatorstop();
      if (xhr.status === 200) {
        
        var responseJSON = JSON.parse(xhr.response);
        console.log("responseJSON"+JSON.stringify(responseJSON));
        if(responseJSON['statusCode']==0)
        {
          displayMicClassifiers(responseJSON['classifiers']);
        }
          
      }
      
  };
  xhr.onerror = function()
  {
    ajaxindicatorstop();
    
    
  };
  
  xhr.open('GET', '/iot_device/micPhoneClassifiers/');
  xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  xhr.setRequestHeader("X-CSRFToken", csrf_token);
  
  xhr.send();
  }
}

function displayMicClassifiers(classifiers)
{
  console.log("displayMicClassifiers");
    micClassifierUserList = classifiers;
    var table = document.getElementById('mic_classifier_user_list');
    
    for (var i = 0; i < classifiers.length; i++) 
      var row = table.insertRow(-1);  
      {   
        var classifier = classifiers[i];
        console.log("classifier "+JSON.stringify(classifier));
        
        var cell = row.insertCell(-1);
        cell.innerHTML = "<input style='cursor:pointer' value='"+classifier["classifier"]+"'"+
          " onclick='micClassifierSelected(this)' readonly>"
        
      }
  
}

function micClassifierSelected(element)
{
  
  document.getElementById('mic_classifier').value=element.value;
}



