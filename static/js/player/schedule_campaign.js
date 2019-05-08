 function exportScheduleReports()
 {


    var dev_id = document.getElementById('selectBox').value;
    var from_date = document.getElementById('datepicker_from').value;
    var to_date = document.getElementById('datepicker_to').value;
    var start_time = document.getElementById('start_time').value;
    var end_time = document.getElementById('end_time').value;

    if(dev_id != "None"){
    if(from_date == null || from_date == "" || start_time == null || start_time == "")
    {
      swal("Please select start date and time");
    }else if(to_date==null || to_date == "" || end_time == null || end_time == ""){
      swal("Please select end date and time");
    }
    
    if (Date.parse(from_date) > Date.parse(to_date)) {
      swal("Can not have an end time earlier than your start time")
      return false;
    }

   // alert(dev_id+" "+from_date+" "+to_date);
	
    }else{

	alert(dev_id+" "+from_date+" "+to_date);
    alert("succes");
		
    //    displayInitUploadBusyDialog();
    //    var xhr = new XMLHttpRequest();
    //    var params = 'accessToken=web&player='+dev_id+'&from_date='+from_date+'&to_date='+to_date;
    
    // xhr.onload = function() {
    //    dismissBusyDialog();
    //     if (xhr.status === 200) {
            
    //       var blob = new Blob([xhr.response], { type: 'octet/stream' });

    //       var link = document.createElement('a');
    //       link.href = window.URL.createObjectURL(blob);
    //       link.download = "campaignReports("+from_date+"-"+to_date+").xlsx";

    //       document.body.appendChild(link);

    //       link.click();

    //       document.body.removeChild(link);
            
    //     }
    //     else {
    //         var errorMessage = xhr.response || 'Unable to upload file';
         
    //         console.log(errorMessage);
    //         swal("unable to upload - "+errorMessage);
    //     }


    //   };
    //    xhr.onerror = function()
    //   {
    //     dismissBusyDialog();
    //     swal('No internet');
    //   };

    // xhr.open('POST', '/player/exportCampaignReports/');
     
    // xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

    // xhr.setRequestHeader("X-CSRFToken", csrf_token );
    // xhr.responseType = "arraybuffer";
    // xhr.send(params);
    }
 }
