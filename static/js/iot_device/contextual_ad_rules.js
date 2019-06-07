
var campaignsList=[];
var playersList=[];

function showRuleCreationBtn() 
 {
	var creation_btn = document.getElementById("create_btn");
	var deviceId=document.getElementById("dev_id");
    if(deviceId.value=="0")
    {
     creation_btn.style.display = "none";  
    }
    else{
    creation_btn.style.display = "block";
	document.getElementById("submit_btn").style.display="none";
	document.getElementById("rules_form").style.display="none";
         
    }

}

function displayRulesCreationForm()
{
	var creation_btn = document.getElementById("create_btn");
	var submit_btn=document.getElementById("submit_btn");

	creation_btn.style.display ="none";
	submit_btn.style.display="block";
	document.getElementById("rules_form").style.display="block";

    displayCampaignsList();
	if(playersList!=null)
	{

	}else
	{
         carpGetPlayersList();
	}

}


//to get the campaigns list
function carpGetCampaigns()
  {
    try {
       
    $.ajax(
    {

      type:'POST',
      url: '/campaigns/list_my_campaigns/',
      headers: {            
            'X-CSRFToken':'{{ csrf_token }}'
        },
      data:{
                secretKey: 'web',
                
      },
      
      success: function(data)
       {
        
        if(data['statusCode']==0)
        {
        	campaignsList=data['campaigns'];
             
            displayCampaignsList();
           
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
  function carpGetPlayersList()
  {
    try {
       
    $.ajax(
    {

      type:'POST',
      url: '/player/getPlayers/',
      headers: {            
            'X-CSRFToken':'{{ csrf_token }}'
        },
      data:{
                accessToken: 'web',
                
      },
     
      success: function(data)
       {
        
        if(data['statusCode']==0)
        {
             
            carpDisplayCampaigns(data['players']);
           
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

  function displayCampaignsList()
  {

	if(campaignsList!=null && campaignsList.length>0)
	{

        for (var i = 0; i < campaignsList.length; i++) 
        {
          
        }
      
	}else
	{
          carpGetCampaigns();
	}

  }

  function displayPlayersList()
  {
  	if(playersList!=null && playersList.length>0)
  	{
  		for (var i = 0; i < playersList.length; i++) 
        {
          
        }
  	}else
	{
          carpGetPlayersList();
	}


  }

