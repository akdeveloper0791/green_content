 var selectedWeekDays = [];

 function display_reports(response)
 {

  var table = document.getElementById("sc_rec_table");
  var row = table.insertRow(0);
  row.id="sc_rec_row_"+response.schedules['id'];

  //var cell1 = row.insertCell(0);
  
row.innerHTML='<div class="container" style="background-color: #F7F6F6; border: .2px solid #F7F6F6; margin: 1%;position: relative;">'+
         '<div style="color:gray;">Schedule From:<span class="user_data" >'+response.schedules['schedule_from']+'</span></div>'+
         '<div style="color:gray;">Schedule From:<span class="user_data" >'+response.schedules['schedule_to']+'</span></div>'+
         '<div style="color:gray;">Schedule Priority :<span class="user_data" >'+response.schedules['sc_priority']+'</span></div>'+
         '<div style="color:gray;width:76%; line-height: 1.45;display:inline-block;float: left;">Repeates :<span class="user_data" >'+
         getScheduleType(response.schedules['schedule_type'],response.schedules['additional_info'])+'</span></div>'+
         '<span class="fa fa-trash"  style="cursor:pointer;color:orangered; display:inline-block;width:4%;float: left;margin-left: 01.5%;margin-right: 01.5%; "onclick="deleteSC('+response.schedules['id']+')"></span>'+
         '<div  style="color:lawngreen;width:6%;margin-right:5px; display:inline-block;float: left;margin-left: 01.5%;margin-right: 01.5%;">ACTIVE</div>'+
         '</div>'      

}
 



 function saveSchedule(pc_id)
 {
    
    var dev_id = document.getElementById('selectBox').value;
    var from_date = document.getElementById('datepicker_from').value;
    var to_date = document.getElementById('datepicker_to').value;
    var start_time = document.getElementById('start_time').value;
    var end_time = document.getElementById('end_time').value;
    var priority = document.getElementById('sc_priority').value;
    var additionalInfo = null;
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
		if(dev_id=="350")
    {
      console.log("selectedWeekDays size"+selectedWeekDays.length);
      if(selectedWeekDays.length<=0)
      {
        swal("Please select any one of the week days");
        return false;
      }else
      {
        var weekDaysArray = {'weekDays':selectedWeekDays};
        
        additionalInfo = JSON.stringify(weekDaysArray);
      }
    }
       ajaxindicatorstart("<img src='/static/images/ajax-loader.gif'><br/> Please wait...!");

       // displayInitUploadBusyDialog();
       var xhr = new XMLHttpRequest();
       var params = 'access_token=web&schedule_from='+fromDate+'&schedule_to='+toDate+'&pc_id='+pc_id+'&schedule_type='+dev_id+'&sc_priority='+priority+
       '&additional_info='+additionalInfo;
    
    
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


function toggleWeekDaySelection(daybutton)
{
  var weekdayIndex = selectedWeekDays.indexOf(daybutton.value);
  if(weekdayIndex>=0)
  {
    daybutton.className = "select_week_days_default";
    selectedWeekDays.splice(weekdayIndex,1);
  }else
  {
    selectedWeekDays.push(daybutton.value);
    daybutton.className = "select_week_days_selected";
  }

  console.log("selectedWeekDays"+JSON.stringify(selectedWeekDays));
   
}

function onRepeatChange()
{
   var onRepeatValue = document.getElementById("selectBox").value;
   if(onRepeatValue == "350")
   {
     document.getElementById('weekly_repeat_days_div').style.display ="block"
   }else
   {
    document.getElementById('weekly_repeat_days_div').style.display ="none"
   }
}




function getScheduleType(schduleType,additionalInfo)
{
  var type;
  switch(parseInt(schduleType))
  {
    case 100:
    type="None";
    break;
   
    case 110:
    type="Per Minute";
    break;

    case 120:
    type="Hourly";
    break;

    case 200:
    type="Daily";
    break;

    case 350://Weekly will have additionalInfo day wise
     type=getWeeklyInfo(additionalInfo);
    break;

    case 250:
    type="Monthly";
    break;
   
    case 300:
    type="Yearly";
    break;

   default:
     type="None";
      break;

  }
  return type;

}

function getWeeklyInfo(additionalInfo)
{
  var extraInfo="";var preAppend="";

 var responseObj =JSON.parse(additionalInfo.replace(/&quot;/g,'"'));

 if (responseObj!=null) 
 {
  for (i in responseObj.weekDays)
        { 
            extraInfo += preAppend+ getWeekDaysInfo(responseObj.weekDays[i]);
            preAppend=",";
        } 

 }else
 {
  extraInfo= "None";
 }
 
 return extraInfo;
}


function getWeekDaysInfo(dayInfo)
{
   var day="";
   switch(parseInt(dayInfo))
   {
    case 1:
     day="Sun";
     break;

     case 2:
     day="Mon";
     break;
     
     case 3:
     day="Tue";
     break;
    
    case 4:
     day="Wed";
     break;

   case 5:
     day="Thu";
     break;

   case 6:
     day="Fri";
     break;

   case 7:
     day="Sat";
     break;

     default:
     day="None";
     break;
   }

return day;
}


