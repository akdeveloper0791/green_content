

 function display_reports(response){
// var m_result = schedules;
  


 //  console.log("display"+m_result.length);
 //  if(m_result.length>=0){
 // console.log("display"+m_result.length);

 // var new_rows="";
    
    // var table = document.getElementById('reports_table');
    
// var schedule = JSON.stringify(response.schedules);  
//console.log(response.schedules['id']);
  var table = document.getElementById("reports_table");
  var row = table.insertRow(0);
  var cell1 = row.insertCell(0);
  var cell2 = row.insertCell(1);
  var cell3 = row.insertCell(2);
  var cell4 = row.insertCell(3);
   var cell5 = row.insertCell(4);
  cell1.innerHTML = response.schedules['id'];
  cell2.innerHTML = response.schedules['schedule_from'];
  cell3.innerHTML = response.schedules['schedule_to'];
  cell4.innerHTML = "<span style='color:lawngreen'>ACTIVE</span>";
  cell5.innerHTML = "<span class='fa fa-trash' style='cursor:pointer;color:orangered'></span>";
  
   // for (var metrics in response.schedules) 
   //  {
   //     console.log("display"+metrics);  
       
   //  row = table.insertRow(-1);
   //       var cell = row.insertCell(-1);
   //       cell.innerHTML = metrics.id;
   //       cell.style.color = "#5FCF80";
   //       cell.style.fontWeight = "bold";
         
   //       var cell = row.insertCell(-1);
   //       cell.innerHTML = metrics.schedule_from;
   //       // var cell = row.insertCell(-1);
   //       // if(campaignId>=1)
   //       // {
   //       //   cell.innerHTML = "<a href='/campaigns/previewCampaign/"+campaignId+"'target='_blank'>"+metrics.campaign_name+"</a>";
   //       // }else
   //       // {
   //       //  cell.innerHTML = metrics.campaign_name;
   //       // }
         
   //       // var duration = metrics.t_duration;
   //       // var no_of_times_played = metrics.t_played;

   //        var cell = row.insertCell(-1);
   //       cell.innerHTML = metrics.schedule_from;

   //         var cell = row.insertCell(-1);
   //       cell.innerHTML = metrics.schedule_from;

   //       var cell = row.insertCell(-1);
   //       cell.innerHTML = metrics.schedule_from;

   //       }
         
    // }



}
 



 function exportScheduleReports(pc_id)
 {


    var dev_id = document.getElementById('selectBox').value;
    var from_date = document.getElementById('datepicker_from').value;
    var to_date = document.getElementById('datepicker_to').value;
    var start_time = document.getElementById('start_time').value;
    var end_time = document.getElementById('end_time').value;

   console.log("Inside exportScheduleReports from_date - "+from_date+"to_date"+to_date);
   
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
       var params = 'access_token=web&schedule_from='+fromDate+'&schedule_to='+toDate+'&pc_id='+pc_id+'&schedule_type='+dev_id;
    //swal("Sdfsdf"+xhr.status);
    xhr.onload = function() {
     if (xhr.status === 200) {
            console.log("response in schedule campaign "+xhr.response);

            var responseObj = JSON.parse(xhr.response);
           
            // Upload succeeded. Do something here with the file info.
            // dismissInitBusyDialog();

            if(responseObj.statusCode == 0)
            {
              // dismissBusyDialog();
               display_reports(responseObj);
               console.log(responseObj.schedules);
               //swal(responseObj.status);

              
            }else
            {
              
              //document.getElementById('metrix_list').innerHTML = responseObj.status;
              // dismissBusyDialog();
              swal(responseObj.status);
            }

        }
        else {
            var errorMessage = xhr.response || 'Unable to update';
            // Upload failed. Do something here with the error.
            console.log(errorMessage);
            swal("unable to update - "+errorMessage);
        }


      };
       xhr.onerror = function()
      {
        //dismissBusyDialog();
        swal('No internet');
      };

    xhr.open('POST', '/campaigns/saveScheduleCampaign/');
     
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

    xhr.setRequestHeader("X-CSRFToken", csrf_token );
    
    xhr.send(params);
    
 }
