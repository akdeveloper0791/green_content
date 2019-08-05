
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

function displayDGPlayersInfo(data ,group_id)
{
  var isPlayersAssigned=false;
  carSelectedPlayers=[];
  
  document.getElementById('ctad_rule_id').value =rule_id;
  document.getElementById('rule_name').innerHTML=data['rule'].classifier;

  document.getElementById('dg_players').style.display="block";
   var dvTable = document.getElementById("ctadr_player_list");

   var players=data['devices']
    
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


