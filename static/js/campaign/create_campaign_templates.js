
function cctDisplayTemplates()
{
	if(isMobileBrowser())
	{
		document.getElementById('cct_display_template_modal_mobile').
	   style.display="block";
	}else
	{
		document.getElementById('cct_display_template_modal').
	   style.display="block";
	}
	
	
}

function cctDismissTemplates()
{
	
	if(isMobileBrowser())
	{
		document.getElementById('cct_display_template_modal_mobile').
	   style.display="none";
	}else
	{
		document.getElementById('cct_display_template_modal').
	   style.display="none";
	}
}