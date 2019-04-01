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

function displayBusyDialog(msg)
{
	document.getElementById("init_upload_busy_dialg_div").style.display = "block"; 
	document.getElementById('busy_dialog').style.display="block";
	document.getElementById('busy_dialog_msg').innerHTML = msg;
	document.getElementById('busy_dialog_msg').value = msg;
}

function dismissBusyDialog()
{
  $('#busy_dialog').modal('hide');
  document.getElementById("init_upload_busy_dialg_div").style.display = "none"; 
	document.getElementById('busy_dialog').style.display="none";
}
