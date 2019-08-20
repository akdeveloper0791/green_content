function displayGroupPlayers(players)
{
  console.log("displayGroupPlayers");
  var dvTable = document.getElementById("group_info_players");
  //init existing players
  existedPlayers=[];

  if(players.length>=1)
  {

     var table = document.createElement("TABLE");
     table.id="group_info_players_TABLE";
     table.border = "0";
     table.style.borderSpacing = "20px";
     for (var i = 0; i < players.length; i++) 
      {
         player = players[i];
         row = table.insertRow(-1);
         row.id = "player_row_"+player.player_id;
        
         existedPlayers.push(player.player_id);
         var cell = row.insertCell(-1);
         cell.innerHTML =player.player__name;
              
         var deleteCell = row.insertCell(-1);
         deleteCell.innerHTML = "<input type='image' src='/static/images/ic_remove.png' alt='remove' title='remove' onclick='removePlayers("+player.player_id+")'>"
         
      }
    dvTable.innerHTML = "";
    dvTable.appendChild(table);  
 
  }else
    {
      //no campaigns
      dvTable.innerHTML = "No Players";
    }
}

function displayPlayersToAdd()
{
  closeGroupInfo();
  lmpcbListPlayers();
}

function sendLMPCBselectedPlayers()
{
  closeLmpcbPlayers();
  assignPlayersApi(lmpcbselectedPlayers);
}

function assignPlayersApi(players)
{
    
  try {
        ajaxindicatorstart("<img src='/static/images/ajax-loader.gif'><br/> Please wait...!");

    $.ajax(
    {

      type:'POST',
      url: '/groups/assignPlayers/',
      headers: {            
            'X-CSRFToken':csrf_token
        },

      data:{
                accessToken: 'web',
                g_id: document.getElementById('group_info_id').value,
                players:JSON.stringify(players)
                
      },
      
      success: function(data)
       {
         ajaxindicatorstop();
       
       
              swal(data['status']);
              if(data['statusCode']==0)
              {
                lmpcbselectedPlayers =[];
                getGroupInfo(document.getElementById('group_info_id').value);
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

function removePlayers(playerId)
  {
    players = [playerId];
    
    try {
        ajaxindicatorstart("<img src='/static/images/ajax-loader.gif'><br/> Please wait...!");

    $.ajax(
    {

      type:'POST',
      url: '/groups/removePlayers/',
      headers: {            
            'X-CSRFToken':csrf_token
        },

      data:{
                accessToken: 'web',
                g_id: document.getElementById('group_info_id').value,
                players:JSON.stringify(players)
                
      },
      
      success: function(data)
       {
         ajaxindicatorstop();
         swal(data['status']);
         if(data['statusCode']==0)
          {
             var table = document.getElementById("group_info_players_TABLE");
             //after delete ,, check and delete rows
             for(var i=0;i<players.length;i++)
             {
                try
                {
                  var row = document.getElementById("player_row_"+players[i]);
                 

                  table.deleteRow(row.rowIndex);

                  //remove from existing campaigns
                var index = existedPlayers.indexOf(players[i]);
                if (index > -1) {
                  existedPlayers.splice(index, 1);
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
