
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
   console.log("createGroup:"+groupName);

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
         console.log("createGroup response:"+JSON.stringify(data));
         swal(data['status']); 
         dismissGroupCreationForm(); 
         displayDeviceGroups();
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
  document.getElementById('submit_btn').style.display="none";
  document.getElementById('create_btn').style.display="block";
  document.getElementById('group_name').value="";
  document.getElementById('dg_creation_form').style.display="none";
}

//display device groups
function displayDeviceGroups()
{

}