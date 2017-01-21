
   function setCookie(cname,cvalue,exdays){
      var d = new Date();
      d.setTime(d.getTime()+(exdays*24*60*60*1000));
      var expires = "expires="+d.toGMTString();
      document.cookie = cname+"="+cvalue+"; "+expires;
   }
   function getCookie(cname){
      var name = cname + "=";
      var ca = document.cookie.split(';');
      for(var i=0; i<ca.length; i++) {
         var c = ca[i].trim();
         if (c.indexOf(name)==0) return c.substring(name.length,c.length);
      }
      return "";
   }
   function checkCookie(){
      var latesttime=getCookie("latesttime");
      if (latesttime!=""){
         console.log(latesttime); 
      }
      else {
         latesttime = (new Date()).getTime();
         if (latesttime!="" && latesttime!=null){
            setCookie("latesttime",latesttime,30);
         }
      }
   }
   function add0(m){return m<10?'0'+m:m }
   function format(shijianchuo)
   {
   //shijianchuo是整数，否则要parseInt转换
   var time = new Date(shijianchuo);
   var y = time.getFullYear();
   var m = time.getMonth()+1;
   var d = time.getDate();
   var h = time.getHours();
   var mm = time.getMinutes();
   var s = time.getSeconds();
   return y+'-'+add0(m)+'-'+add0(d)+' '+add0(h)+':'+add0(mm)+':'+add0(s);
   }
   function formatToTamp(stringTime)
   {
      var timestamp = Date.parse(new Date(stringTime));
      return timestamp;
   }
$(document).ready(function() {

Highcharts.setOptions({                                                     
global: {                                                               
   useUTC: false                                                       
}                                                                       
});  
  URL = "http://218.244.147.240";
  PORT = "4020";
   var chart = {                                                                
	type: 'spline',                                                     
	animation: Highcharts.svg, // don't animate in old IE               
	marginRight: 10,                                                    
	events: {                                                           
		load: function() {                                              
																		
			// set up the updating of the chart each second             
			var series = this.series[0];                                
			setInterval(function() {    
            
            var latest_time = getCookie("latesttime");
             console.log(latest_time+"!!!!");
            if(latest_time!=""&&latest_time!=undefined)
            {
                console.log("latest_time is not null");

            }else
            {
               latest_time = format((new Date()).getTime());
               setCookie("latesttime",format((new Date()).getTime()),30);
               console.log("latest_time is null");
            }
            var x = (new Date()).getTime(); // current time                             
				    y = Math.random();
            console.log(latest_time);
            $.getJSON("/starttime",{
            latesttime: latest_time,
            b: 12},
            function (result) {

                latest_time = getCookie("latesttime");
                console.log("json test"); 
                var list=result.result;
                console.log(latest_time);
                console.log(list);
                if(latest_time!=""&&latest_time!=undefined)
                {
                   if(list.length!=0)
                   {
                     setCookie("latesttime",list[list.length-1].timestamp,30);//将返回结果中最=大的时间缓存到cookie中，过期时间默认30天
                     for(var i =0;i<list.length;i++)
                     {
                        x = formatToTamp(list[i].timestamp);
                        y = list[i].value;
                        series.addPoint([x, y], true, true);
                     }
                   }
                }
                else
                {
                  //cookie为空
                  console.log("starttime is null!!!!");
                  setCookie("latesttime",format((new Date()).getTime()),30);
                  var latest_time = getCookie("latesttime");
                  console.log(latest_time);
                }
             });	
	             
			}, 1000);                                                   
		}                                                               
	}                                                                   
	};

   var title = {
       text: '实时曲线'   
   };
   var subtitle = {
        text: 'realtime curve'
   };
   var xAxis = {
 			type: 'datetime',                                                   
			tickPixelInterval: 100   
   };
   var yAxis = {
      title: {
         text: '测量结果'
      },
      plotLines: [{
         value: 0,
         width: 1,
         color: '#808080'
      }]
   };   

   var tooltip = {
      	formatter: function() {                                             
			return '<b>'+ this.series.name +'</b><br/>'+                
			Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) +'<br/>'+
			Highcharts.numberFormat(this.y, 2);                         
	}  
   };

   var legend = {
      layout: 'vertical',
      backgroundColor: '#FFFFFF',
      align: 'right',
      verticalAlign: 'top',
      borderWidth:0,
      x:0,
      y:30
   };

   var series =  [
      {                                                              
		name: 'IDC',                                                
		data: (function() {                                                 
			// generate an array of random data                             
			var data = [],                                                  
				time = (new Date()).getTime(),                              
				i;                                                          
																			
			for (i = -19; i <= 0; i++) {                                    
				data.push({                                                 
					x: time + i * 1000,                                     
					y: Math.random()                                        
				});                                                         
			}                                                               
			return data;                                                    
		   })()                                                                
      }
   ];

   var json = {};

   json.title = title;
   json.subtitle = subtitle;
   json.xAxis = xAxis;
   json.yAxis = yAxis;
   json.tooltip = tooltip;
   json.legend = legend;
   json.series = series;
   json.chart = chart;

   $('#container').highcharts(json);
});
