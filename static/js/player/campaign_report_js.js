var selectedFilterPartners = [];
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
         
         row = table.insertRow(-1);
         var cell = row.insertCell(-1);
         cell.innerHTML = metrics.campaign_owner;

         var cell = row.insertCell(-1);
         cell.innerHTML = metrics.player__name;
         cell.style.color = "#5FCF80";
         cell.style.fontWeight = "bold";
         
         var campaignId = metrics.campaign_id;
         
         var cell = row.insertCell(-1);
         if(campaignId>=1)
         {
           cell.innerHTML = "<a href='/campaigns/previewCampaign/"+campaignId+"'target='_blank'>"+metrics.campaign_name+"</a>";
         }else
         {
          cell.innerHTML = metrics.campaign_name;
         }
         
         var duration = metrics.t_duration;
         var no_of_times_played = metrics.t_played;

         var cell = row.insertCell(-1);
         cell.innerHTML = no_of_times_played;

         var cell = row.insertCell(-1);
         cell.innerHTML = (duration);
         
         try
         {
          if(metrics.last_played_at!=null)
           {
           var date = new Date(metrics.last_played_at);
           date = date.getDate()+"-"+(date.getMonth()+1)+"-"+date.getFullYear() + " "+date.getHours()+":"+date.getMinutes()+":"+date.getSeconds();

           var cell = row.insertCell(-1);
           cell.innerHTML = (date);
          }
         }catch(err)
         {

         }
         
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
  
    $("#reports_table").find("tr:not(:first)").remove();

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
    if(selectedFilterPartners.length>=1)
    {
      params += '&partners='+JSON.stringify(selectedFilterPartners);
    }
    

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
            console.log(errorMessage);
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

 function exportCampaignReports()
 {
  
    $("#reports_table").find("tr:not(:first)").remove();

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
       if(selectedFilterPartners.length>=1)
        {
          params += '&partners='+JSON.stringify(selectedFilterPartners);
        }
    xhr.onload = function() {
       //dismissInitBusyDialog();
       dismissBusyDialog();
        if (xhr.status === 200) {
            
          var blob = new Blob([xhr.response], { type: 'octet/stream' });

          var link = document.createElement('a');
          link.href = window.URL.createObjectURL(blob);
          link.download = "campaignReports("+from_date+"-"+to_date+").xlsx";

          document.body.appendChild(link);

          link.click();

          document.body.removeChild(link);
            
        }
        else {
            var errorMessage = xhr.response || 'Unable to upload file';
            // Upload failed. Do something here with the error.
            console.log(errorMessage);
            swal("unable to upload - "+errorMessage);
        }


      };
       xhr.onerror = function()
      {
        dismissBusyDialog();
        swal('No internet');
      };

    xhr.open('POST', '/player/exportCampaignReports/');
     
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

    xhr.setRequestHeader("X-CSRFToken", csrf_token );
    xhr.responseType = "arraybuffer";
    xhr.send(params);
    }
 }

 function onPartnerSelect(selectButton)
 {
   var selected = selectButton.value;
   selectedFilterPartners = [];
   if(selected=="All")
   {
    
   }else
   {
    selectedFilterPartners.push(selected);
   }
   console.log("On partner selected "+selected);
   console.log("Selected partners list"+JSON.stringify(selectedFilterPartners));
 }
