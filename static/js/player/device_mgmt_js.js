

function getCampaignInfo(playerId)
{
  try {
        ajaxindicatorstart("<img src='/static/images/ajax-loader.gif'><br/> Please wait...!");
       
		$.ajax(
		{

		  type:'POST',
		  url: '/player/campaigns/',
		  headers: {		        
		        'X-CSRFToken': csrf_token
		    },
		  data:{
                accessToken: 'web',
                pId: playerId,
                
		  },
		  
		  success: function(data)
		   {
		   	 ajaxindicatorstop();
			console.log("data"+JSON.stringify(data));
            
            if(data['statusCode']==0)
		    {
             
             displayCampaignInfo(data,playerId);
            
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

function displayCampaignInfo(info,pId)
{
     document.getElementById('campaigns_info_player').innerHTML=document.getElementById(pId+"_player_name").innerHTML;
     document.getElementById('player_campaign_info_id').value=pId;
     displayPlayerCampaigns(info['campaigns'],pId);
	 var modal = document.getElementById('campaigns_info');
	  modal.style.display = "block";
 
}

function displayPlayerCampaigns(campaigns,pId)
{
	var dvTable = document.getElementById("player_info_campaigns");
    
    //init existing campaigns
    existedCampaigns=[];

    if(campaigns.length>=1)
    {
        //Create a HTML Table element.
		 var table = document.createElement("TABLE");
		 table.id="player_info_campaigns_TABLE";
		 table.classList.add("info","table-hover")
		 table.border = "0";
		 table.style.borderSpacing = "20px";
		 
		 //Get the count of columns.
		  var columnCount = 5;

		    
		  for (var i = 0; i < campaigns.length; i++) 
		  {
		     campaign = campaigns[i];
             row = table.insertRow(-1);
             row.id = "campaign_row_"+campaign.id;
             existedCampaigns.push(campaign.id);

             {

              var cell = row.insertCell(-1);

               //cell.style.float="l";
               //cell.style.text-align="left";
             
                cell.innerHTML =campaign.campaign_name;
                 cell.id="cell_"+campaign.id
              
               
              //skip toggle 
              var cell = row.insertCell(-1);

              if((campaign['is_skip']==1?true:false)==true)
              {
              	cell.innerHTML = '<div style="margin:10px;"> <label class="switch switch-yes-no">'+
					'<input class="switch-input" type="checkbox" checked onclick="skipCampaign(this,'+campaign.id+','+pId+');"/>'+
					'<span class="switch-label" data-on="Skipped" data-off="Skip"></span>'+ 
					'<span class="switch-handle"></span> </label> </div>'
				}else
				{
					cell.innerHTML = '<div style="margin:10px"> <label class="switch switch-yes-no">'+
					'<input class="switch-input" type="checkbox"  onclick="skipCampaign(this,'+campaign.id+','+pId+');"/>'+
					'<span class="switch-label" data-on="Skipped" data-off="Skip"></span>'+ 
					'<span class="switch-handle"></span> </label> </div>'
				}

				var campaign_type=campaign.camp_type
				if(campaign_type==2)
				{
                var scheduleCell = row.insertCell(-1);
                scheduleCell.innerHTML = "<a class='fa fa-calendar' href='/player/schedule_campaign/"+pId+"/"+campaign.id+"' alt='Schedule' title='Schedule' style='cursor:pointer;margin:10px;visibility: hidden;'></a>";
		
				}else
				{
					var scheduleCell = row.insertCell(-1);
                scheduleCell.innerHTML = "<a class='fa fa-calendar' href='/player/schedule_campaign/"+pId+"/"+campaign.id+"' alt='Schedule' title='Schedule' style='cursor:pointer;margin:10px;'></a>";
		
				}

              
              var deleteCell = row.insertCell(-1);
              deleteCell.innerHTML = "<span class='fa fa-trash' alt='Remove' style='margin:10px;' title='Remove' onclick='campDeleteAlertDialog("+campaign.id+")'></span>";             
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

	closePlayerCampaignInfo();
    lmcbListCampaigns();	 
}

function closePlayerCampaignInfo()
{
	document.getElementById('campaigns_info').style.display="none";
}



function sendLMCBselectedCampaigns()
{
	closeLmcbCampaigns();
    assignCampaignsApi(lmcbselectedCampaigns);
}

function assignCampaignsApi(campaigns)
{
		
 try {
       ajaxindicatorstart("<img src='/static/images/ajax-loader.gif'><br/> Please wait...!");

		$.ajax(
		{

		  type:'POST',
		  url: '/player/assignCampaigns/',
		  headers: {		        
		        'X-CSRFToken': csrf_token
		    },

		  data:{
                accessToken: 'web',
                pId: document.getElementById('player_campaign_info_id').value,
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
              	getCampaignInfo(document.getElementById('player_campaign_info_id').value);
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


function campDeleteAlertDialog(campId)
{
    var cell = document.getElementById("cell_"+campId);
	 document.getElementById('campaign_alert_dialog').style.display = "block";
     document.getElementById('camp_name').innerHTML='<h5><b>Campaign Name:</b><span style="color:blue;">'+cell.innerText+'</span></h5>';
     var submitBtn = document.getElementById('delete_camp_btn');

     //submitBtn.onclick=removeCampaign(campId);
     submitBtn.innerHTML = "<button style='background-color:transparent;border:transparent;' id='delete_camp_btn' onclick='removeCampaign("+campId+")'>Yes,delete it!</button>"

}

function closeCampaignAlertDialog()
{
	document.getElementById('campaign_alert_dialog').style.display = "none";
}


function removeCampaign(campaignId)
{
	closeCampaignAlertDialog();

		campaigns = [campaignId];
		
		try {
        ajaxindicatorstart("<img src='/static/images/ajax-loader.gif'><br/> Please wait...!");

		$.ajax(
		{
		  type:'POST',
		  url: '/player/removeCampaigns/',
		  headers: {		        
		        'X-CSRFToken': csrf_token 
		    },

		  data:{
                accessToken: 'web',
                pId: document.getElementById('player_campaign_info_id').value,
                campaigns:JSON.stringify(campaigns)
                
		  },
		  
		  success: function(data)
		   {
		   	 ajaxindicatorstop();
			  
              swal(data['status']);
              if(data['statusCode']==0)
              {
              	var table = document.getElementById("player_info_campaigns_TABLE");

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



function skipCampaign(checkbox,cId,pId)
{
  try {
        ajaxindicatorstart("<img src='/static/images/ajax-loader.gif'><br/> Please wait...!");
       
		$.ajax(
		{

		  type:'POST',
		  url: '/player/skipCampaigns/',
		  headers: {		        
		        'X-CSRFToken': csrf_token
		    },
		  data:{
                accessToken: 'web',
                pId: pId,
                cId:cId,
                is_skip:(checkbox.checked==true?1:0)
                
		  },
		  
		  success: function(data)
		   {
		   	 ajaxindicatorstop(); 

            if(data['statusCode']==0)
		    {
             
             //displayCampaignInfo(data,playerId);
            
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
    	ajaxindicatorstop();
		alert(Exception.message);
	}	
}

function getLastPlayerAccessedTime(serverTime)
{
	console.log(serverTime);
  if(serverTime!=null)
  {
    
  
    var date = new Date(serverTime);
    serverTime = date.toLocaleString();
    date = new Date(serverTime+" GMT");
    return date.toLocaleString();
  }else
  {
    return null;
  }
  
}




