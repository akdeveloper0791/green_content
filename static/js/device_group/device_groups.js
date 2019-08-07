var playersList=[];
var dgSelectedPlayers=[];

function displayGroupCreationForm() 
{
	var creation_btn = document.getElementById("create_btn");
	var submit_btn=document.getElementById("submit_btn");
	creation_btn.style.display ="none";
	submit_btn.style.display="block";

	document.getElementById("dg_creation_form").style.display="block";
	// body...
}

function createGroup()
{
	//validations 
  var groupName = document.getElementById("group_name").value;
  if(groupName=="" || groupName==null)
  {
    swal("Please enter valid group name");
    return false;
  }


 try {
   ajaxindicatorstart("<img src='/static/images/ajax-loader.gif'><br/> Please wait...!");    
    $.ajax(
    {

      type:'POST',
      url: '/device_group/create/',
      headers: {            
            'X-CSRFToken':csrf_token
        },
      data:{
           accessToken: 'web',
           name: groupName,  
      },
     
      success: function(data)
       {
        ajaxindicatorstop();
        if(data['statusCode']==0)
        {
     
         swal(data['status']); 
         dismissGroupCreationForm(); 
         location.reload(true);
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

function dismissGroupCreationForm()
{
  document.getElementById('create_btn').style.display="block";
  document.getElementById('group_name').value="";
  document.getElementById('dg_creation_form').style.display="none";
}



function groupDeleteAlertDialog(groupId)
{
    var cell = document.getElementById("group_"+groupId);
	 document.getElementById('group_delete_dialog').style.display = "block";
     document.getElementById('dg_name').innerHTML='<h5><b>Group name:</b><span style="color:blue;">'+cell.innerText+'</span></h5>';
     var submitBtn = document.getElementById('delete_group_btn');

     //submitBtn.onclick=removeCampaign(campId);
     submitBtn.innerHTML = "<button style='background-color:transparent;border:transparent;' id='delete_group_btn' onclick='deleteDeviceGroup("+groupId+")'>Yes,delete it!</button>"

}

function closeGroupDeleteDialog()
{
	document.getElementById('group_delete_dialog').style.display = "none";
}


function deleteDeviceGroup(groupId)
{
	closeGroupDeleteDialog();
  try {
   ajaxindicatorstart("<img src='/static/images/ajax-loader.gif'><br/> Please wait...!");    
    $.ajax(
    {

      type:'POST',
      url: '/device_group/delete/',
      headers: {            
            'X-CSRFToken':csrf_token
        },
      data:{
           accessToken: 'web',
           dg_id: groupId,
              
      },
     
      success: function(data)
       {
        ajaxindicatorstop();
        if(data['statusCode']==0)
        {

        	swal(data['status']); 
            deleteGroupInfo(groupId);
           
        }
        else
       {
             swal(data['status']);                         
       }

    
       },
    
     error: function (jqXHR, exception) {
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


function deleteGroupInfo(groupId)
{
    
    document.getElementById("groups_info").deleteRow(document.getElementById(groupId+"_group_name").rowIndex);
}

function getGroupPlayersInfo(group_id)
{
  try {
        ajaxindicatorstart("<img src='/static/images/ajax-loader.gif'><br/> Please wait...!");
       
    $.ajax(
    {

      type:'POST',
      url: '/device_group/getInfo',
      headers: {            
            'X-CSRFToken': csrf_token
        },
      data:{
                accessToken: 'web',
                dg_id: group_id,
                is_devices:true,
                
      },
      
      success: function(data)
       {
         ajaxindicatorstop();
           
        if(data['statusCode']==0)
        {
           console.log("displayDGPlayersInfo:"+JSON.stringify(data));
           displayDGPlayersInfo(data,group_id);       
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

function displayDGPlayersInfo(data,group_id)
{
	var data ,group_id;
  //var isPlayersAssigned=false;
    dgSelectedPlayers=[];
  
  document.getElementById('device_group_id').value =group_id;
  document.getElementById('dg_player_name').innerHTML=data['info'].name;
   

   document.getElementById('dg_players').style.display="block";
   var dvTable = document.getElementById("dg_player_list");

   var players=data['devices']
    
    if(players.length>=0)
    {
            //Create a HTML Table element.
         var table = document.createElement("TABLE");
         table.classList.add("data","table-hover"); 
       
      for (var i = 0; i < players.length; i++) 
        {

          var player = players[i];
          // player_list.push(player.id);
              row = table.insertRow(-1);
             {
              var cell = row.insertCell(-1);
              
    
           var dgDeviceId = players[i]['dg_device_Id'];
              
              if(dgDeviceId>0)
              {
               //isPlayersAssigned=true;
                cell.innerHTML = "<input id='dgp_cb_"+player.id+"' type='checkbox' checked= true disabled= true style='margin:5px;cursor:pointer;' name='name1' onchange='dgpOnchange(this,"+player['id']+")'/>";
              }else
              {
                cell.innerHTML = "<input type='checkbox' style='margin:5px;cursor:pointer;'  name='name1' onchange='dgpOnchange(this,"+players[i]['id']+")'/>";
              }
              
              var cell = row.insertCell(-1);
               cell.innerHTML =player.name;

              if(dgDeviceId>0)
              {
                var deleteCell = row.insertCell(-1);
                deleteCell.innerHTML = "<input type='image'style='cursor:pointer;' id='dgp_unassign_"+player.id+"'src='/static/images/ic_remove.png' alt='remove' title='remove' onclick='dgPlayerRemove("+players[i]['id']+")'>"  
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
function dgpOnchange(element,playerId)
 {
  if(element.checked == true)//check and add player Id to newPlayers List
  {
      if(dgSelectedPlayers.includes(playerId)==false)
      {
        dgSelectedPlayers.push(playerId);
      }

  }else
  {
    dgRemoveSelectedPlayer(playerId)
  }
  
 }

 function dgRemoveSelectedPlayer(playerId)
 {
    //if player id is in new players list check and remove it
      var elementIndex = dgSelectedPlayers.indexOf(playerId);
       if(elementIndex>=0)
      {
      dgSelectedPlayers.splice(elementIndex,1);
      }  
  
 }


 function assignDGselectedPlayers()
 {
  closeDeviceGroupPlayers();
  if(dgSelectedPlayers.length>=1)
  {
    
    ajaxindicatorstart("<img src='/static/images/ajax-loader.gif'><br/> Please wait...!");
  var xhr = new XMLHttpRequest();
    xhr.onload = function() {
      ajaxindicatorstop();
      if (xhr.status === 200) {
       
        var responseJSON = JSON.parse(xhr.response);
        if(responseJSON['statusCode']==0)
        {
          
          getGroupPlayersInfo(document.getElementById('device_group_id').value);
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
    
  };
  
  xhr.open('POST', '/device_group/assignPlayers/');
  xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  xhr.setRequestHeader("X-CSRFToken", csrf_token);
  
  
    var params = 'gId='+document.getElementById('device_group_id').value+'&players='+JSON.stringify(dgSelectedPlayers)+
     '&accessToken=web';
     
    xhr.send(params);
    
  }
   
 }


function dgPlayerRemove(playerId)
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
          dgRemoveSelectedPlayer(playerId);

          document.getElementById('dgp_cb_'+playerId).disabled=false;
          document.getElementById('dgp_cb_'+playerId).checked=false;

          document.getElementById('dgp_unassign_'+playerId).style.display="none";
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
    
  };
  
  xhr.open('POST', '/device_group/removePlayers/');
  xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  xhr.setRequestHeader("X-CSRFToken", csrf_token);
  
  
    var params = 'players='+JSON.stringify(players)+'&gId='+document.getElementById('device_group_id').value+
     '&accessToken=web';
     
    xhr.send(params);

}

function closeDeviceGroupPlayers()
{
  document.getElementById('dg_players').style.display="none";
  //newPlayersList=[];
 
}


function getDGCampaignsInfo(group_id)
{ 
  try {
        ajaxindicatorstart("<img src='/static/images/ajax-loader.gif'><br/> Please wait...!");
       
    $.ajax(
    {

      type:'POST',
      url: '/device_group/getInfo',
      headers: {            
            'X-CSRFToken': csrf_token
        },
      data:{
                accessToken: 'web',
                dg_id: group_id,
                is_campaigns:true,
                
      },
      
      success: function(data)
       {
         ajaxindicatorstop();
           
        if(data['statusCode']==0)
        {
       
        displayDGCampaignInfo(data,group_id);       
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

function displayDGCampaignInfo(data,groupId)
{
	var modal = document.getElementById('dg_campaigns_dialog');
     modal.style.display = "block";
     document.getElementById('dg_campaign_name').innerHTML=data['info'].name;
     document.getElementById('group_campaign_info_id').value=groupId;
     displayGroupsCampaigns(data['campaigns'],groupId);
   
}

function displayGroupsCampaigns(campaigns,groupId)
{
  var dvTable = document.getElementById("group_assigned_campaigns");
    
    //init existing campaigns inside Rule
    existedCampaigns=[];

    if(campaigns.length>=1)
    {
        //Create a HTML Table element.
     var table = document.createElement("TABLE");
     table.id="group_info_campaigns_TABLE";
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

              var cell = row.insertCell(-1);
              cell.innerHTML =campaign.campaign__campaign_name;

             
              var deleteCell = row.insertCell(-1);
              deleteCell.innerHTML = "<span class='fa fa-trash' alt='Remove' title='Remove' style='cursor:pointer;color:orangered; display:inline-block; margin: 10px;' onclick='removeCampaign("+campaign.campaign__id+")'>"            
           

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
   closeDGCampaignsDialog();
    lmcbListCampaigns();   
}

function closeDGCampaignsDialog()
{
  document.getElementById('dg_campaigns_dialog').style.display="none";
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
      url: '/device_group/assignCampaigns/',
      headers: {            
            'X-CSRFToken': csrf_token
        },

      data:{
                accessToken: 'web',
                gId: document.getElementById('group_campaign_info_id').value,
                campaigns:JSON.stringify(campaigns)
                
      },
      
      success: function(data)
       {
         ajaxindicatorstop();
       
       
              swal(data['status']);
              if(data['statusCode']==0)
              {
                lmcbselectedCampaigns =[];
                getDGCampaignsInfo(document.getElementById('group_campaign_info_id').value);
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
      url: '/device_group/removeCampaigns/',
      headers: {            
            'X-CSRFToken': csrf_token 
        },

      data:{
                accessToken: 'web',
                //is_campaigns:true,
                gId: document.getElementById('group_campaign_info_id').value,
                campaigns:JSON.stringify(campaigns)
                
      },
      
      success: function(data)
       {
         ajaxindicatorstop();
        
              swal(data['status']);
              if(data['statusCode']==0)
              {
                var table = document.getElementById("group_info_campaigns_TABLE");

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


