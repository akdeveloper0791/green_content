

function showRuleCreationBtn() 
 {
	var creation_btn = document.getElementById("create_btn");
	var dev_id=document.getElementById("dev_id");
    if(dev_id.value=="0")
    {
     creation_btn.style.display = "none";  
    }
    else{
          creation_btn.style.display = "block";
    }

}

function displayRulesCreationForm()
{
	var creation_btn = document.getElementById("create_btn");
	var submit_btn=document.getElementById("submit_btn");

	creation_btn.style.display ="none";
	submit_btn.style.display="block";
	document.getElementById("rules_form").style.display="block";
}

function lmcbGetCampaigns()
  {
    try {
        ajaxindicatorstart("<img src='{% static "images/ajax-loader.gif" %}'><br/> Please wait...!");

    $.aja
    {

      type:'POST',
      url: '/campaigns/list_my_campaigns/',
      headers: {            
            'X-CSRFToken':'{{ csrf_token }}'
        },
      data
                secretKey: 'web',
                
      },
      
      success: function(data)
       {
         ajaxindicatorstop();
        

        if(data['statusCode']==0)
        {
             
            lmcbDisplayCampaigns(data['campaigns']);      
        }
       else
       {

           swal(data['status']);                               
       }

       },
    
     error: function (jqXHR, exception) {
      ajaxindicatorstop();
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

