

 function display_reports(response)
 {

  var table = document.getElementById("sc_rec_table");
  var row = table.insertRow(0);
  row.id="sc_rec_row_"+response.schedules['id'];

  //var cell1 = row.insertCell(0);
  
row.innerHTML='<div class="container" style="background-color: #F7F6F6; border: .2px solid #F7F6F6; margin: 1%;position: relative;">'+
         '<div style="color:gray;">Schedule From:<span class="user_data" >'+response.schedules['schedule_from']+'</span></div>'+
         '<div style="color:gray;">Schedule From:<span class="user_data" >'+response.schedules['schedule_to']+'</span></div>'+
         '<div id="schedule_priority" style="color:gray;width:76%; line-height: 1.45;display:inline-block;">Schedule Priority :<span class="user_data" >1</span></div>'+
         '<span id="delete_schedule" class="fa fa-trash"  style="cursor:pointer;color:orangered; display:inline-block;width:4%; "onclick="deleteSC('+response.schedules['id']+')"></span>'+
         '<div id="schedule_status" style="color:lawngreen;width:6%;margin-right:5px; display:inline-block;">ACTIVE</div>'+
         '</div>'
         /*<div id="schedule_to" style="color:gray;">Schedule To :<span class="user_data" >{{ schedule.schedule_to}}</span></div>  

        <div id="schedule_priority" style="color:gray;width:76%; line-height: 1.45;
       display:inline-block;">Schedule Priority :<span class="user_data" >1</span></div>
        <span id="delete_schedule" class="fa fa-trash"  style="cursor:pointer;color:orangered;
       display:inline-block;width:4%; "onclick="deleteSC({{ schedule.id}})"></span>
         <div id="schedule_status" style="color:lawngreen;width:6%;margin-right:5px;
       display:inline-block;">ACTIVE</div>   
      </div>'*/
 
  
   

}
 



 function saveSchedule(pc_id)
 {
    ajaxindicatorstart("<img src='/static/images/ajax-loader.gif'><br/> Please wait...!");

    var dev_id = document.getElementById('selectBox').value;
    var from_date = document.getElementById('datepicker_from').value;
    var to_date = document.getElementById('datepicker_to').value;
    var start_time = document.getElementById('start_time').value;
    var end_time = document.getElementById('end_time').value;
    var priority = document.getElementById('sc_priority').value;
    
    if(Number.isInteger(parseInt(priority)) == false)
    {
      priority = 0;
    }
   
    // if(dev_id != "None"){
    if(from_date == null || from_date == "" || start_time == null || start_time == "")
    {
      swal("Please select start date and time");
       return false;
    }else if(to_date==null || to_date == "" || end_time == null || end_time == ""){
      swal("Please select end date and time");
       return false;
    }
    
    if (Date.parse(from_date) > Date.parse(to_date)) {
      swal("Can not have an end time earlier than your start time")
      return false;
    }

    var d = new Date(from_date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2) month = '0' + month;
    if (day.length < 2) day = '0' + day;

    var fromDate = [year, month, day].join('-');

        var d = new Date(to_date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2) month = '0' + month;
    if (day.length < 2) day = '0' + day;

    var toDate = [year, month, day].join('-');

    //alert(fromDate+" "+toDate+" "+dev_id+" "+from_date+" "+to_date);
	
    // }else{
    fromDate = fromDate+" "+start_time+":00";
    toDate = toDate+" "+end_time+":00";
    //alert(fromDate+ " "+toDate+" "+pc_id+" "+dev_id);
		
       // displayInitUploadBusyDialog();
       var xhr = new XMLHttpRequest();
       var params = 'access_token=web&schedule_from='+fromDate+'&schedule_to='+toDate+'&pc_id='+pc_id+'&schedule_type='+dev_id+'&sc_priority='+priority;
    
    
    //swal("Sdfsdf"+xhr.status);
    xhr.onload = function() {
     if (xhr.status === 200) {
      ajaxindicatorstop();
            console.log(xhr.response);
            var responseObj = JSON.parse(xhr.response);
           
            // Upload succeeded. Do something here with the file info.
            // dismissInitBusyDialog();

            if(responseObj.statusCode == 0)
            {
              // dismissBusyDialog();
               display_reports(responseObj);
               //console.log(responseObj.schedules);
               //swal(responseObj.status);

              
            }else
            {
              
              //document.getElementById('metrix_list').innerHTML = responseObj.status;
              // dismissBusyDialog();
              ajaxindicatorstop();
              swal(""+(responseObj.status));
            }

        }
        else {
          ajaxindicatorstop();
            var errorMessage = xhr.response || 'Unable to update';
            // Upload failed. Do something here with the error.
            console.log(errorMessage);
            swal("unable to update - "+errorMessage);
        }


      };
       xhr.onerror = function()
      {
        ajaxindicatorstop();
        //dismissBusyDialog();
        swal('No internet');
      };

    xhr.open('POST', '/campaigns/saveScheduleCampaign/');
     
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

    xhr.setRequestHeader("X-CSRFToken", csrf_token );
    
    xhr.send(params);
    
 }

function deleteSC(scId)
{
  ajaxindicatorstart("<img src='/static/images/ajax-loader.gif'><br/> Please wait...!");
  
  var xhr = new XMLHttpRequest();
  var params = 'access_token=web&sc_id='+scId;
    
  xhr.onload = function() {
   if (xhr.status === 200) {
      ajaxindicatorstop();
      var responseObj = JSON.parse(xhr.response);
      if(responseObj.statusCode == 0)
      {
        deleteSCRow(scId);
               
      }else
      {
        swal(""+(responseObj.status));
      }

    }
    else {
      ajaxindicatorstop();
            var errorMessage = xhr.response || 'Unable to update';
            
            swal("unable to delete - "+errorMessage);
        }


      };
       xhr.onerror = function()
      {
        ajaxindicatorstop();
        //dismissBusyDialog();
        swal('No internet');
      };

    xhr.open('POST', '/campaigns/deleteScheduleCampaign/');
     
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

    xhr.setRequestHeader("X-CSRFToken", csrf_token );
    
    xhr.send(params);
}

function deleteSCRow(scId)
{
    console.log("delete sc row "+scId);
    document.getElementById("sc_rec_table").deleteRow(document.getElementById("sc_rec_row_"+scId).rowIndex);
}
