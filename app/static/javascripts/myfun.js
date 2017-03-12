 function queryhistory(starttime,endtime)
 {

   $.getJSON("/history_data",{
          starttime:starttime,endtime:endtime,token:18d54ec8446d03451f5552033c64dbda,
          b: 12},
          function (result) {
               var list=result.result;
               console.log(list);
               for(var i =0;i<list.length;i++)
               {
                  time = formatToTamp(list[i].timestamp);
                  value = list[i].value;
                  var datatype = list[i].datatype;
                  var danwei;
                  if(datatype=="VDC"||datatype=="VAC")
                      danwei="KV";
                  else if(datatype=="IAC"||datatype=="IDC")
                      danwei = "mA";


                  //添加表格行
                  var row = document.getElementById("table_id").insertRow();
                  var cell;
                  cell = row.insertCell(-1);
                  cell.innerHTML =  datatype;
                  cell.align = "center";

                  cell = row.insertCell(-1);
                  cell.innerHTML = formatToTamp(list[i].timestamp);
                  cell.align = "center";

                  cell = row.insertCell(-1);
                  cell.innerHTML = list[i].value+danwei;
                  cell.align = "center";

                  cell = row.insertCell(-1);
                  cell.innerHTML = list[i].separation;
                  cell.align = "center";                    
               }      
           });    
  }