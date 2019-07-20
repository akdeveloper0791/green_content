var displayMetrics = "metrics";
var isMobileBrowser = isMobileBrowser();
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
	if(!isMobileBrowser)
	{

	//displayAgeBarReports([],[]);
	//displayAgeBarReports([],[]);	
	}
	
	document.getElementById("web_graphs").style.display="none"; 
    document.getElementById("web_trends").style.display="none"; 
		
}

function displayGraphs()
{
	if(isMobileBrowser)
	{
		var elmnt = document.getElementById("mobile_graphs");
		if(elmnt.style.display=="none")
		{
			elmnt.style.display="block";
			elmnt.scrollIntoView();
		}
		
	    
	}else
	{
	  
	  document.getElementById("web_graphs").style.display="block"; 	
	}
}

function displayAgeBarReports(labels,data)
{
	var canvas = document.getElementById("bar_reports_cnv");
	if(isMobileBrowser)
	{
      canvas = document.getElementById("bar_reports_cnv_mobile");
	}
	new Chart(canvas, {
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



function highliteSelectedMetrics(metrics,selectedButtonId)
{
	if(metrics!=displayMetrics)
	{
       displayMetrics = metrics;
       //deactivate change the class name
       var x = document.getElementsByClassName("selected_metrics");
		
		for (var i = 0; i < x.length; i++) {
		  x[i].className = "gradient-button gradient-btn";
		}
	}

	if(isMobileBrowser)
	{
		if(metrics=="metrics")
	   {
		var elmnt = document.getElementById("mobile_graphs");
		if(elmnt.style.display=="none")
		{
			elmnt.style.display="block";
			elmnt.scrollIntoView();
		}
	    }else if(metrics=="trends"){
       var elmnt = document.getElementById("mobile_trends");
		if(elmnt.style.display=="none")
		{
			elmnt.style.display="block";
			elmnt.scrollIntoView();
		}
        }
           
	}
	if(metrics=="metrics")
	{
document.getElementById("web_graphs").style.display="block";
document.getElementById("web_trends").style.display="none";
	}else if(metrics=="trends")
	{
document.getElementById("web_graphs").style.display="none";
document.getElementById("web_trends").style.display="block";

	}

document.getElementById(selectedButtonId).className="selected_metrics"
}

function showAnalytics(isAutoRefresh=false)
{   
	highliteSelectedMetrics("metrics","analytics_view");
	
	dismissTabularView();
	
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
    	from_date,to_date,isAutoRefresh);
    
    generateGenderAgeBarCharts(dev_id,
    	from_date,to_date,isAutoRefresh);
    
    //generateGenderLineCharts(dev_id,from_date,to_date,isAutoRefresh);
    
    generateAgeBarCharts(dev_id,
    	from_date,to_date,isAutoRefresh);
	
}


function showTrends(isAutoRefresh=false)
{
	highliteSelectedMetrics("trends","trends_view");
	
	dismissTabularView();
	
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

    generateGenderLineCharts(dev_id,from_date,to_date,isAutoRefresh); 
}

function generateAgeBarCharts(dev_id,from_date,to_date,isAutoRefresh)
{
	//get reports 
	try {
		 displayGraphsProgressbar();
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
		   		dismissGraphsProgressbar();
		   	//ajaxindicatorstop();
			
            if(data['statusCode']==0)
		    {

		     displayGraphs();
             displayAgeBarReports(data['labels'],data['data']);
             
            
			}
			else
			{
             if(!isAutoRefresh)
             {
             	swal(data['status']);
             }
             
                                    
			}

		   },
		
		 error: function (jqXHR, exception) {
		 	//ajaxindicatorstop();
		 		dismissGraphsProgressbar();
		 	alert(exception+jqXHR.responseText);
		 }

		});
	}
	catch(Exception)
    {
		alert(Exception.message);
	}
}

function generateGenderPieCharts(dev_id,from_date,to_date,isAutoRefresh)
{
   //get reports 
	try {
        //ajaxindicatorstart("<img src='/static/images/ajax-loader.gif'><br/> Please wait...!");
       displayGraphsProgressbar();
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
		   	dismissGraphsProgressbar();
		   	//ajaxindicatorstop();
			console.log(JSON.stringify(data));
            if(data['statusCode']==0)
		    {
             displayGenderPieCharts(data['labels'],data['data']);
            
			}
			else
			{
             if(!isAutoRefresh)
             {
             swal(data['status']);	
             }
             
                                    
			}

		   },
		
		 error: function (jqXHR, exception) {
		 		dismissGraphsProgressbar();
		 	//ajaxindicatorstop();
		 	//alert(exception+jqXHR.responseText);
		 }

		});
	}
	catch(Exception)
    {
		//alert(Exception.message);
	}	
}

function displayGenderPieCharts(labels,data)
{
	var canvas = document.getElementById("gender_pie_reports_cnv");
	if(isMobileBrowser)
	{
		canvas = document.getElementById("gender_pie_reports_cnv_mobile");
	}

	new Chart(canvas, {
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

function generateGenderAgeBarCharts(dev_id,from_date,to_date,isAutoRefresh)
{
   //get reports 
	try {
		displayGraphsProgressbar();
        //ajaxindicatorstart("<img src='/static/images/ajax-loader.gif'><br/> Please wait...!");
       
		$.ajax(
		{

		  type:'POST',
		  url: '/iot_device/vm_age_gender_bar_reports',
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
		   	dismissGraphsProgressbar();
            if(data['statusCode']==0)
		    {
             displayGenderAgeCharts(data['labels'],data['f_data'],
             	data['m_data']);
            
			}
			else
			{
             if(!isAutoRefresh)
             {
             //swal(data['status']);	
             }
                                   
			}

		   },
		
		 error: function (jqXHR, exception) {
		 		dismissGraphsProgressbar();
		 	//ajaxindicatorstop();
		 	//alert(exception+jqXHR.responseText);
		 }

		});
	}
	catch(Exception)
    {
		//alert(Exception.message);
	}	
}

function displayGenderAgeCharts(labels,femaleData,maleData)
{
	var canvas = document.getElementById("gender_age_chart_grouped");
	if(isMobileBrowser)
	{
		canvas = document.getElementById("gender_age_chart_grouped_mobile");
	}
	new Chart(canvas, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: "Female",
          backgroundColor: "#8e5ea2",
          data: femaleData
        }, {
          label: "Male",
          backgroundColor: "#3e95cd",
          data: maleData
        }
      ]
    },
    options: {
      title: {
        display: true,
        text: 'Gender and Age based metrics'
      }
    }
});
}

function generateGenderLineCharts(dev_id,from_date,to_date,isAutoRefresh)
{
   //get reports 
	try {

		displayTrendsProgressbar();
        //ajaxindicatorstart("<img src='/static/images/ajax-loader.gif'><br/> Please wait...!");
       
		$.ajax(
		{

		  type:'POST',
		  url: '/iot_device/vm_gender_line_reports',
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
		     dismissTrendsProgressbar();
		   	//ajaxindicatorstop();
			console.log(JSON.stringify(data));
            if(data['statusCode']==0)
		    {
             displayGenderLineCharts(data['labels'],data['f_graph'],
             	data['m_graph']);
            }
			else
			{
             if(!isAutoRefresh)
             {
      
              swal(data['status']);	

             }
             
                                    
			}

		   },
		
		 error: function (jqXHR, exception) {
		 	//ajaxindicatorstop();
		 		dismissTrendsProgressbar();
		 	if(!isAutoRefresh)
             {
             alert(exception+jqXHR.responseText);
             }
		 	//alert(exception+jqXHR.responseText);
	
		 }

		});
	}
	catch(Exception)
    {

     //dismissProgressbar();
    
    	if(!isAutoRefresh)
        {
		 alert(Exception.message);
		}
	}	
}

function displayGenderLineCharts(labels,femaleData,maleData)
{
	
	var canvas = document.getElementById("gender_line");
	if(isMobileBrowser)
	{
		canvas = document.getElementById("gender_line_mobile");
	}
	new Chart(canvas, {
	  type: 'line',
	  data: {
	    labels: labels,
	    datasets: [{ 
	        data: femaleData,
	        label: "Female",
	        borderColor: "#3e95cd",
	        fill: true
	      }, { 
	        data: maleData,
	        label: "Male",
	        borderColor: "#8e5ea2",
	        fill: true
	      }, 
	    ]
	  },
	  options: {
	    title: {
	      display: true,
	      text: 'Gender based metrics'
	    }
	  }
	});
}

function displayTrendsProgressbar()
{
document.getElementById("trends_prog_bar").style.display="block";
}

function dismissTrendsProgressbar()
{
document.getElementById("trends_prog_bar").style.display="none";
}


function displayGraphsProgressbar()
{
document.getElementById("graphs_prog_bar").style.display="block";
}

function dismissGraphsProgressbar()
{
document.getElementById("graphs_prog_bar").style.display="none";
}