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
