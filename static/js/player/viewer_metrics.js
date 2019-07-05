function dismissTabularView()
{
	document.getElementById("tabular_display").style.display="none";
}

function displayTabularView()
{
	document.getElementById("tabular_display").style.display="block";
}
function dismissGraphs()
{
	document.getElementById("analytics_grpahs1").style.display="none";
}

function displayGraphs()
{
	if(isMobileBrowser())
	{
		var wrapperElm = document.getElementById("analytics_grpahs1");
        wrapperElm.style.display="block";
        wrapperElm.class="";
        document.getElementById("age_bar_reports").class="";
        document.getElementById("gender_reports").class="";
	    wrapperElm.scrollIntoView();
	}else
	{
	 document.getElementById("analytics_grpahs1").style.display="flex";	
	}
	
}

function displayAgeBarReports(labels,data)
{
	//document.getElementById("age_bar_reports").style.display="inline-block";
	new Chart(document.getElementById("bar_reports_cnv"), {
	    type: 'bar',
	    data: {
	      labels: labels,
	      datasets: [
	        {
	          label: "",
	          backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
	          data: data
	        }
	      ]
	    },
	    options: {
	      legend: { display: false },
	      title: {
	        display: true,
	        text: 'Age based metrics(in numbers)'
	      }
	    }
	});

}
function showAnalytics()
{   
	dismissTabularView();
	dismissGraphs()
	displayGraphs();

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
    }

    generateGenderPieCharts(dev_id,
    	from_date,to_date);

	//get reports 
	try {
        //ajaxindicatorstart("<img src='/static/images/ajax-loader.gif'><br/> Please wait...!");
       
		$.ajax(
		{

		  type:'POST',
		  url: '/iot_device/vm_bar_reports',
		  headers: {		        
		        'X-CSRFToken': csrf_token
		    },
		  data:{
                accessToken: 'web',
                player: dev_id,
                from_date:from_date,
                to_date:to_date
                
		  },
		  
		  success: function(data)
		   {
		   	//ajaxindicatorstop();
			console.log("data"+JSON.stringify(data));
            
            if(data['statusCode']==0)
		    {
             displayAgeBarReports(data['labels'],data['data']);
             //displayCampaignInfo(data,playerId);
            
			}
			else
			{

             swal(data['status']);
                                    
			}

		   },
		
		 error: function (jqXHR, exception) {
		 	//ajaxindicatorstop();
		 	alert(exception+jqXHR.responseText);
		 }

		});
	}
	catch(Exception)
    {
		alert(Exception.message);
	}
}

function generateGenderPieCharts(dev_id,from_date,to_date)
{
   //get reports 
	try {
        //ajaxindicatorstart("<img src='/static/images/ajax-loader.gif'><br/> Please wait...!");
       
		$.ajax(
		{

		  type:'POST',
		  url: '/iot_device/vm_gender_pie_reports',
		  headers: {		        
		        'X-CSRFToken': csrf_token
		    },
		  data:{
                accessToken: 'web',
                player: dev_id,
                from_date:from_date,
                to_date:to_date
                
		  },
		  
		  success: function(data)
		   {
		   	//ajaxindicatorstop();
			console.log("data"+JSON.stringify(data));
            
            if(data['statusCode']==0)
		    {
             displayGenderPieCharts(data['labels'],data['data']);
            
			}
			else
			{

             swal(data['status']);
                                    
			}

		   },
		
		 error: function (jqXHR, exception) {
		 	//ajaxindicatorstop();
		 	alert(exception+jqXHR.responseText);
		 }

		});
	}
	catch(Exception)
    {
		alert(Exception.message);
	}	
}

function displayGenderPieCharts(labels,data)
{
	//document.getElementById("gender_reports").style.display="inline-block";
	new Chart(document.getElementById("gender_pie_reports_cnv"), {
	    type: 'pie',
	    data: {
	      labels: labels,
	      datasets: [{
	        label: "in number",
	        backgroundColor: ["#3e95cd", "#8e5ea2"],
	        data: data
	      }]
	    },
	    options: {
	      title: {
	        display: true,
	        text: 'Gender based metrics(in numbers)'
	      }
	    }
    });
}