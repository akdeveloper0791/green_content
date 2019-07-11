var displayMetrics = "metrics";

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
	if(!isMobileBrowser())
	{

	//displayAgeBarReports([],[]);
	//displayAgeBarReports([],[]);	
	}
	
	document.getElementById("web_graphs").style.display="none"; 	
}

function displayGraphs()
{
	if(isMobileBrowser())
	{
		var ageBarReports = document.getElementById("age_bar_reports");
		ageBarReports.width="1000";
		ageBarReports.height="1000";

		var genderReports = document.getElementById("gender_reports");
		genderReports.width="1000";
		genderReports.height="1000";

		var ageBarReports = document.getElementById("gender_age_bar_reports");
		ageBarReports.width="1000";
		ageBarReports.height="1000";

		var ageBarReports = document.getElementById("gender_age_line_reports");
		ageBarReports.style.width="1000";
		ageBarReports.style.height="1000";

        /*document.getElementById("age_bar_reports").class="";
        document.getElementById("gender_reports").class="";
        document.getElementById("gender_age_bar_reports").class="";
        document.getElementById("gender_age_line_reports").class="";
 
	    wrapperElm.scrollIntoView();*/
	    document.getElementById("web_graphs").style.display="block";
	}else
	{
	  
	  document.getElementById("web_graphs").style.display="block"; 	
	}
}

function displayGraphs1()
{
	if(isMobileBrowser())
	{
		var wrapperElm = document.getElementById("analytics_grpahs1");
        wrapperElm.style.display="block";
        wrapperElm.class="";

        var graphs2  = document.getElementById("analytics_grpahs2");
        graphs2.style.display="block";
        graphs2.class="";

        var graphs3  = document.getElementById("analytics_grpahs3");
        graphs3.style.display="block";
        graphs3.class="";

        document.getElementById("age_bar_reports").class="";
        document.getElementById("gender_reports").class="";
        document.getElementById("gender_age_bar_reports").class="";
        document.getElementById("gender_age_line_reports").class="";

	    wrapperElm.scrollIntoView();
	}else
	{
	 var graphsDiv1 = document.getElementById("analytics_grpahs1");
	 var graphsDiv2 = document.getElementById("analytics_grpahs2");
	 if(graphsDiv1.style.display=="none")
	 {
       graphsDiv1.style.display = "flex";
	 }

	 if(graphsDiv2.style.display=="none")
	 {
       graphsDiv2.style.display = "flex";
	 }

	 var graphsDiv3 = document.getElementById("analytics_grpahs3");
	 if(graphsDiv3.style.display=="none")
	 {
       graphsDiv3.style.display = "flex";
	 }
	 	
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
    
    generateGenderLineCharts(dev_id,
    	from_date,to_date,isAutoRefresh);
    
    generateAgeBarCharts(dev_id,
    	from_date,to_date,isAutoRefresh);
	
}

function generateAgeBarCharts(dev_id,from_date,to_date,isAutoRefresh)
{
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

function generateGenderAgeBarCharts(dev_id,from_date,to_date,isAutoRefresh)
{
   //get reports 
	try {
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

function displayGenderAgeCharts(labels,femaleData,maleData)
{
	//document.getElementById("gender_reports").style.display="inline-block";
	new Chart(document.getElementById("gender_age_chart_grouped"), {
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
             //swal(data['status']);	
             }
             
                                    
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

function displayGenderLineCharts(labels,femaleData,maleData)
{
	
	//document.getElementById("gender_reports").style.display="inline-block";
	new Chart(document.getElementById("gender_line"), {
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