function displayInitUploadBusyDialog()
{
  $("#busy_dialog").modal();
  
  document.getElementById("busy_dialog_header").style.display = "none";

  document.getElementById("init_upload_busy_dialg_div").style.display = "block"; 
  
}

function dismissInitBusyDialog()
{
  document.getElementById("init_upload_busy_dialg_div").style.display = "none"; 

  //$('#busy_dialog').modal('toggle');
}

function dismissBusyDialog()
{
  $('#busy_dialog').modal('hide');
}

function display_reports(responseObj){
	var m_result = responseObj.metrics;
	
	var dvTable = document.createElement("div");


	if(m_result.length>=0){


     document.getElementById('metrix_list').innerHTML = "";
     var new_rows="";
    
    var table = document.getElementById('reports_table');

		for (var i = 0; i < m_result.length; i++) 
		{
		     var metrics = m_result[i];
         
         var date = new Date(metrics.created_at);
         date = date.getDate()+"-"+date.getMonth()+"-"+date.getFullYear() + " "+date.getHours()+":"+date.getMinutes()+":"+date.getSeconds();

		     //new_rows += '<tr><td style="color:#5FCF80;font-weight: bold">'+metrics.player__name+'</td><td>'+date+'</td><td>'+metrics.g_male+'</td><td>'+metrics.g_female+'</td><td>'+metrics.age_0_2+'</td><td>'+metrics.age_4_6+'</td><td>'+metrics.age_8_12+'</td><td>'+metrics.age_15_20+'</td><td>'+metrics.age_25_32+'</td><td>'+metrics.age_38_43+'</td><td>'+metrics.age_48_53+'</td><td>'+metrics.age_60_100+'</td></tr>';  
         row = table.insertRow(-1);
         var cell = row.insertCell(-1);
         cell.innerHTML = metrics.player__name;

         var cell = row.insertCell(-1);
         cell.innerHTML = metrics.campaign_name;
		     
         var duration = metrics.t_duration;
         var no_of_times_played = metrics.times_played;

         var cell = row.insertCell(-1);
         cell.innerHTML = duration;

         var cell = row.insertCell(-1);
         cell.innerHTML = no_of_times_played;

         var cell = row.insertCell(-1);
         cell.innerHTML = (duration*no_of_times_played);
    }

       		
     //new_rows += new_rows
			 //document.getElementById('metrix_list').innerHTML += new_rows;
         //$("#metrix_list").append(new_rows);
       

	}else{

		  document.getElementById('metrix_list').innerHTML += "No records Found";
	}
}
 
 function listCampaignReports()
 {
  console.log("listCampaignReports");
    var dev_id = document.getElementById('dev_id').value;
    var from_date = document.getElementById('from_date').value;
    var to_date = document.getElementById('to_date').value;
    if(from_date == null || from_date == "")
    {
      swal("please select From_Date");
    }else if(to_date==null || to_date == ""){
      swal("please select To_Date");
    }
    
    if (Date.parse(from_date) > Date.parse(to_date)) {
      swal("Invalid Date Range!\nStart Date cannot be after End Date!")
      return false;
    }else{

       displayInitUploadBusyDialog();
       var xhr = new XMLHttpRequest();
    var params = 'accessToken=web&player='+dev_id+'&from_date='+from_date+'&to_date='+to_date;
    
    xhr.onload = function() {
        if (xhr.status === 200) {
            console.log("xhr.response-"+xhr.response);
            var responseObj = JSON.parse(xhr.response);
            // Upload succeeded. Do something here with the file info.
            dismissInitBusyDialog();

            if(responseObj.statusCode == 0)
            {
              dismissBusyDialog();
               display_reports(responseObj);
            }else
            {
              
              document.getElementById('metrix_list').innerHTML = responseObj.status;
              dismissBusyDialog();
              swal(responseObj.status);
            }
            
        }
        else {
            var errorMessage = xhr.response || 'Unable to upload file';
            // Upload failed. Do something here with the error.
            
            swal("unable to upload - "+errorMessage);
        }


      };
       xhr.onerror = function()
      {
        swal('No internet');
      };

    xhr.open('POST', '/player/getCampaignReports/');
     
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

    xhr.setRequestHeader("X-CSRFToken", csrf_token );
    xhr.send(params);
    }
 }

	/*function viewer_matrics_list(){
		var dev_id = document.getElementById('dev_id').value;
		var from_date = document.getElementById('from_date').value;
		var to_date = document.getElementById('to_date').value;
		if(from_date == null || from_date == "")
		{
			swal("please select From_Date");
		}else if(to_date==null || to_date == ""){
			swal("please select To_Date");
		}
		
		if (Date.parse(from_date) > Date.parse(to_date)) {
			swal("Invalid Date Range!\nStart Date cannot be after End Date!")
			return false;
		}else{

			 displayInitUploadBusyDialog();
			 var xhr = new XMLHttpRequest();
    var params = 'accessToken=web&player='+dev_id+'&from_date='+from_date+'&to_date='+to_date;
    
    xhr.onload = function() {
        if (xhr.status === 200) {
            var responseObj = JSON.parse(xhr.response);
            // Upload succeeded. Do something here with the file info.
            dismissInitBusyDialog();

            if(responseObj.statusCode == 0)
            {
            	dismissBusyDialog();
               display_reports(responseObj);
            }else
            {
              
              document.getElementById('metrix_list').innerHTML = responseObj.status;
              dismissBusyDialog();
              swal(responseObj.status);
            }
            
        }
        else {
            var errorMessage = xhr.response || 'Unable to upload file';
            // Upload failed. Do something here with the error.
            
            swal("unable to upload - "+errorMessage);
        }


    	};
     	 xhr.onerror = function()
		  {
		    swal('No internet');
		  };

    xhr.open('POST', '/player/getCampaignReports');
     
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

    xhr.setRequestHeader("X-CSRFToken", csrf_token );
    xhr.send(params);
		}
		
	}*/
