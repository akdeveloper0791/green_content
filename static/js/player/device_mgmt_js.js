
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
     displayPlayerCampaigns(info['campaigns']);
	 var modal = document.getElementById('campaigns_info');
	  modal.style.display = "block";
 
}

function displayPlayerCampaigns(campaigns)
{
	var dvTable = document.getElementById("player_info_campaigns");
    
    //init existing campaigns
    existedCampaigns=[];

    if(campaigns.length>=1)
    {
        //Create a HTML Table element.
		 var table = document.createElement("TABLE");
		 table.id="player_info_campaigns_TABLE";
		 table.classList.add("info")
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
              cell.innerHTML =campaign.campaign_name;
              
              var deleteCell = row.insertCell(-1);
              deleteCell.innerHTML = "<input type='image' src='/static/images/ic_remove.png' alt='remove' title='remove' onclick='removeCampaign("+campaign.id+")'>"
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

function removeCampaign(campaignId)
{
	
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



