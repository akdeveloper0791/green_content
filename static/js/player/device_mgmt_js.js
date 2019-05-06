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
              
              var scheduleCell = row.insertCell(-1);
              scheduleCell.innerHTML = "<span class='fa fa-calendar' onclick='scheduleCampaign("+campaign.id+")' alt='Schedule' title='Schedule' style='cursor:pointer;'></span>";

              var deleteCell = row.insertCell(-1);
              deleteCell.innerHTML = "<span class='fa fa-trash' alt='Remove' title='Remove' onclick='removeCampaign("+campaign.id+")'>"             
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

function closeScheduleCampaignInfo()
{
	document.getElementById('scheduleCampaign').style.display="none";
	formatDate() ;
	 $("#get_date").trigger('click');
    $("#get_date").trigger('click');
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


function scheduleCampaign(campaignId){
document.getElementById("campaigns_info").style.display="none";
document.getElementById("scheduleCampaign").style.display="block";
formatDate();

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

 function exportScheduleReports()
 {


    var dev_id = document.getElementById('selectBox').value;
    var from_date = document.getElementById('from_date').value;
    var to_date = document.getElementById('to_date').value;

    if(dev_id=="Custom"){
    if(from_date == null || from_date == "")
    {
      swal("please select From_Date");
    }else if(to_date==null || to_date == ""){
      swal("please select To_Date");
    }
    
    if (Date.parse(from_date) > Date.parse(to_date)) {
      swal("Invalid Date Range!\nStart Date cannot be after End Date!")
      return false;
    }
    alert(dev_id+" "+from_date+" "+to_date);
	}else{
		alert(dev_id+" "+from_date+" "+to_date);
		
    //    displayInitUploadBusyDialog();
    //    var xhr = new XMLHttpRequest();
    //    var params = 'accessToken=web&player='+dev_id+'&from_date='+from_date+'&to_date='+to_date;
    
    // xhr.onload = function() {
    //    dismissBusyDialog();
    //     if (xhr.status === 200) {
            
    //       var blob = new Blob([xhr.response], { type: 'octet/stream' });

    //       var link = document.createElement('a');
    //       link.href = window.URL.createObjectURL(blob);
    //       link.download = "campaignReports("+from_date+"-"+to_date+").xlsx";

    //       document.body.appendChild(link);

    //       link.click();

    //       document.body.removeChild(link);
            
    //     }
    //     else {
    //         var errorMessage = xhr.response || 'Unable to upload file';
         
    //         console.log(errorMessage);
    //         swal("unable to upload - "+errorMessage);
    //     }


    //   };
    //    xhr.onerror = function()
    //   {
    //     dismissBusyDialog();
    //     swal('No internet');
    //   };

    // xhr.open('POST', '/player/exportCampaignReports/');
     
    // xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

    // xhr.setRequestHeader("X-CSRFToken", csrf_token );
    // xhr.responseType = "arraybuffer";
    // xhr.send(params);
    }
 }
