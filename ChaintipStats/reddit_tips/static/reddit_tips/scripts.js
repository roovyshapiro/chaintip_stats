var countdown_timer;
var countdown_update_label_timer;
var refresh_minutes;
var refresh_seconds;
var checkbox_status;
var selected_date;

//WHEN the page reloads reload the values from local storage
//retrieve_saved_data will also continue the countdown timer
//if the checkbox was enabled before the page was reloaded
window.onload = retrieve_saved_data;

//Called when the page is reloaded
function retrieve_saved_data() {
    checkbox_status = localStorage.getItem("checkbox_status");
    checkbox_status_bool = (checkbox_status == 'true');
    refresh_minutes = localStorage.getItem("refresh_minutes");
    refresh_seconds = refresh_minutes * 60;
    localStorage.setItem("refresh_seconds", refresh_seconds);
    document.getElementById("checkbox_autoupdate").checked = checkbox_status_bool;
    //If the checkbox is already clicked when the page reloads
    if (checkbox_status_bool){
        document.getElementById("auto_update_label").innerHTML = refresh_seconds;
        checkbox_click();
    }
    //Put in today's date into the date selector unless a date has been chosen already
    if (localStorage.getItem("selected_date") == null){
        var today = new Date();
        var month = today.getMonth()+1;
        if(month.toString().length < 2){
          month = '0' + month;
        }
        var today_date = `${today.getFullYear()}-${month}`;
        document.getElementById("date_start").value = today_date;
		localStorage.setItem("selected_date", today_date);
    } else {
        document.getElementById("date_start").value = localStorage.getItem("selected_date");
    }
  }

//
//
//   AUTO-REFRESH BOX + MINUTES SELECTOR
//
//

//WHEN the auto refresh check box is clicked
function checkbox_click() {
    checkbox_status = document.getElementById("checkbox_autoupdate").checked;
    localStorage.setItem("checkbox_status", checkbox_status);
    update_refresh_time();
    if (checkbox_status == true){
        countdown_timer = setTimeout(function() {
            location.reload();
        }, refresh_seconds * 1000);
        countdown_update();
    } else {
        clearTimeout(countdown_timer);
        clearInterval(countdown_update_label_timer);
        document.getElementById("auto_update_label").innerHTML = '';

    }
}

function update_refresh_time() {
    refresh_minutes = 60;
    refresh_seconds = refresh_minutes * 60; 
    localStorage.setItem("refresh_seconds", refresh_seconds);
    localStorage.setItem("refresh_minutes", refresh_minutes);
    clearTimeout(countdown_timer);
    clearInterval(countdown_update_label_timer);
}

//While countdown_timer starts a one time countdown to refresh the page,
//countdown_update_label_timer starts an interval timer that shows
//how much time is remaining before the page refreshes 
function countdown_update(){
    refresh_seconds = parseInt(localStorage.getItem("refresh_seconds"));
    countdown_update_label_timer = setInterval(function(){
        refresh_seconds -= 1;
        if (refresh_seconds < 1){
            clearInterval(countdown_update_label_timer);
        }
        localStorage.setItem('refresh_seconds', refresh_seconds);
        document.getElementById("auto_update_label").innerHTML = refresh_seconds;
    }, 1000);
}

//When the submit button is clicked on the Dashboard, the 
//date and group are saved to localstorage so it can be retrieved
//after the page is reloaded.
function save_date(){
    selected_date = document.getElementById('date_start').value;
    localStorage.setItem("selected_date", selected_date);
    document.getElementById("date_form").submit();
}

//This function is called when the arrows are clicked next to the timechanger
//to change the date back and forth by one month. This automatically submits the page
//as the submit function was moved to save_date()
function date_changer(timeframe){
    //["2021", "07"]
    var chosen_date_arr = localStorage.getItem('selected_date').split('-');
    //Thu Jul 01 2021 00:00:00 GMT-0400 (Eastern Daylight Time)
    chosen_date = new Date(`${chosen_date_arr[0]},${chosen_date_arr[1]}`);

    if(timeframe=='yesterday'){
      //Don't allow going back further than the minimum month in the date picker
      var min_month_raw = document.getElementById("date_start").min;
      var min_month_raw_arr = min_month_raw.split('-');
      var min_month = new Date(`${min_month_raw_arr[0]},${min_month_raw_arr[1]}`);
      if(chosen_date.getMonth() < min_month.getMonth() || chosen_date.getMonth() == min_month.getMonth()){
        return;
      }else{
        chosen_date.setMonth(chosen_date.getMonth() - 1);
      }
    }

    if(timeframe=='tomorrow'){
      //Don't allow going further than the maximum month in the date picker
        var max_month_raw = document.getElementById("date_start").max;
        var max_month_raw_arr = max_month_raw.split('-');
        var max_month = new Date(`${max_month_raw_arr[0]},${max_month_raw_arr[1]}`);
        if(chosen_date.getMonth() > max_month.getMonth()  || chosen_date.getMonth() == max_month.getMonth()){
            return;
        } else{
            chosen_date.setMonth(chosen_date.getMonth() + 1);
        }
    }

   //1 -> 01, 3 -> 03 etc.
   var month = chosen_date.getMonth() + 1;
   if(month.toString().length == 1){
        month = `0${month}`;
    }

    new_date = `${chosen_date.getFullYear()}-${month}`;
    localStorage.setItem('selected_date', new_date);
    document.getElementById("date_start").value = new_date;
    save_date();
}





//********************** */

//https://datatables.net/
//Data Tables provides built in functionality such as
//sorting, filtering & choosing how many rows to load
$(document).ready( function () {
    $('table.data_table').DataTable();
} );




/*



CHARTS FOR ALL DATA


Rendering a bar chart of all tips per day using ChartsJS
https://docs.djangoproject.com/en/3.1/ref/templates/builtins/#json-script
https://www.chartjs.org/docs/master/samples/bar/vertical.html




*/



try{

  var tips_per_month = JSON.parse(document.getElementById('tip_value_per_month_result').textContent);

  var years = Object.keys(tips_per_month);
  var date_label = [];
  var month_tip_amount = [];
  var month_tip_value = [];
  for (year in years){
    var months = Object.keys(tips_per_month[years[year]]);
    for(month in months){
      date_label.push(`${years[year]} - ${months[month]}`);
      month_tip_amount.push(tips_per_month[years[year]][months[month]]['tip_amount']);
      month_tip_value.push(tips_per_month[years[year]][months[month]]['tip_value']);
  
    }
  }
  
  var year_month_labels = date_label;
  
  var data_tip_per_month = {
    labels: year_month_labels,
    datasets: [{
      label: 'Amount of Tips Per Month',
      data: month_tip_amount,
      backgroundColor:'rgba(30, 144, 255, 0.2)',
      borderColor: 'rgb(25, 25, 112)',
      hoverBackgroundColor:'rgba(255, 205, 86, 0.2)',
      hoverBorderColor:'rgb(255, 205, 86)',
      borderWidth: 1
    }]
  };
  
  var config_tip_per_month = {
      type: 'bar',
      data: data_tip_per_month,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true
          }
        }
      },
    };
  
  var myChart = new Chart(
      document.getElementById('tip_per_month'),
      config_tip_per_month
    );
  
  /* Value per Day instead of tip amount per day */
  var data_tip_value_per_month = {
    labels: year_month_labels,
    datasets: [{
      label: 'Value of Tips (USD) per Month',
      data: month_tip_value,
      backgroundColor:'rgba(252, 108, 133, 0.2)',
      borderColor: 'rgb(147, 61, 65)',
      hoverBackgroundColor:'rgba(255, 205, 86, 0.2)',
      hoverBorderColor:'rgb(255, 205, 86)',
      borderWidth: 1
    }]
  };
  
  var value_config = {
      type: 'bar',
      data: data_tip_value_per_month,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true
          }
        }
      },
    };
  
  var myValueChart = new Chart(
      document.getElementById('value_per_month'),
      value_config
    );
  
  /* Doughnut Chart */
  
  var total_claimed_returned = JSON.parse(document.getElementById('all_stats_total_claimed_returned').textContent);
  var tcr_keys = Object.keys(total_claimed_returned);
  var tcr_values = Object.values(total_claimed_returned);
  
  new Chart(document.getElementById("total_claimed_returned"), {
      type: 'doughnut',
      data: {
        labels: tcr_keys,
        datasets: [
          {
            backgroundColor: ["#191970","#1e90ff","#a9a9a9","#933d41"],
            data: tcr_values
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        title: {
          display: true,
          text: 'Claimed Tips'
        }
      }
  });
  
} catch (e){
  console.log(e);
  console.log("ALL Charts don't work on MONTH Page");
}





/*




CHARTS FOR MONTH DATA


Rendering a bar chart of all tips per day using ChartsJS
https://docs.djangoproject.com/en/3.1/ref/templates/builtins/#json-script
https://www.chartjs.org/docs/master/samples/bar/vertical.html




*/



try{

  var month_tips_per_day = JSON.parse(document.getElementById('month_stats_tip_per_day').textContent);

  var month_keys = Object.keys(month_tips_per_day);
  var month_values = Object.values(month_tips_per_day);
  
  var month_labels = month_keys;
  var month_data = {
    labels: month_labels,
    datasets: [{
      label: 'Amount of Tips Per Day',
      data: month_values,
      backgroundColor:'rgba(30, 144, 255, 0.2)',
      borderColor: 'rgb(25, 25, 112)',
      hoverBackgroundColor:'rgba(255, 205, 86, 0.2)',
      hoverBorderColor:'rgb(255, 205, 86)',
      borderWidth: 1
    }]
  };
  
  
  
  var month_config = {
      type: 'bar',
      data: month_data,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true
          }
        }
      },
    };
  
  var myMonthChart = new Chart(
      document.getElementById('month_tip_per_day'),
      month_config
    );
  
  /* Value per Day instead of tip amount per day */
  
  var month_value_per_day = JSON.parse(document.getElementById('month_stats_value_per_day').textContent);
  
  var month_value_keys = Object.keys(month_value_per_day);
  var month_value_values = Object.values(month_value_per_day);
  
  //Round each item in the fiat_value list to 2 decimal places
  var x = 0;
  var len = month_value_values.length
  while(x < len){ 
    month_value_values[x] = month_value_values[x].toFixed(2); 
      x++
  }
  
  var month_value_labels = month_value_keys;
  var month_value_data = {
    labels: month_value_labels,
    datasets: [{
      label: 'Value of Tips (USD) per Day',
      data: month_value_values,
      backgroundColor:'rgba(252, 108, 133, 0.2)',
      borderColor: 'rgb(147, 61, 65)',
      hoverBackgroundColor:'rgba(255, 205, 86, 0.2)',
      hoverBorderColor:'rgb(255, 205, 86)',
      borderWidth: 1
    }]
  };
  
  var month_value_config = {
      type: 'bar',
      data: month_value_data,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true
          }
        }
      },
    };
  
  var myMonthValueChart = new Chart(
      document.getElementById('month_value_per_day'),
      month_value_config
    );
  
  /* Doughnut Chart */
  
  var month_total_claimed_returned = JSON.parse(document.getElementById('month_stats_total_claimed_returned').textContent);
  var month_tcr_keys = Object.keys(month_total_claimed_returned);
  var month_tcr_values = Object.values(month_total_claimed_returned);
  
  new Chart(document.getElementById("month_total_claimed_returned"), {
      type: 'doughnut',
      data: {
        labels: month_tcr_keys,
        datasets: [
          {
            backgroundColor: ["#191970","#1e90ff","#a9a9a9","#933d41"],
            data: month_tcr_values
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        title: {
          display: true,
          text: 'Claimed Tips'
        }
      }
  });

 
  /*
  Showing how the current tips data compares to the past 3 months
  https://www.chartjs.org/docs/latest/charts/line.html
  Example of Data:
      {
      'October':{
          'first_day': datetime.datetime(2021, 10, 1, 0, 0, tzinfo=<UTC>),
          'last_day': datetime.datetime(2021, 10, 31, 23, 59, 59, tzinfo=<UTC>), 
          'tip_amount': [49, 65, 95, 162, 208, 248, 288, 314, 320, 351, 384, 410, 443, 477, 507, 518, 538, 577, 635, 716, 780, 828, 836, 888, 941, 999, 1035, 1095, 1098]
          }, 
      'September':{
          'first_day': datetime.datetime(2021, 9, 1, 0, 0, tzinfo=<UTC>), 
          'last_day': datetime.datetime(2021, 9, 30, 0, 0, tzinfo=<UTC>), 
          'tip_amount': [28, 66, 66, 66, 86, 154, 169, 203, 254, 305, 322, 393, 434, 439, 456, 481, 519, 549, 575, 610, 632, 645, 669, 697, 717, 746, 776, 792, 798, 816]
      }, 
      'August': {
          'first_day': datetime.datetime(2021, 8, 1, 0, 0, tzinfo=<UTC>), 
          'last_day': datetime.datetime(2021, 8, 31, 0, 0, tzinfo=<UTC>), 
          'tip_amount': [15, 34, 43, 61, 99, 114, 122, 169, 213, 240, 279, 315, 369, 384, 408, 448, 485, 519, 548, 560, 570, 586, 640, 664, 717, 731, 754, 768, 782, 803, 832]
          }, 
      'July': {
          'first_day': datetime.datetime(2021, 7, 1, 0, 0, tzinfo=<UTC>), 
          'last_day': datetime.datetime(2021, 7, 31, 0, 0, tzinfo=<UTC>), 
          'tip_amount': [18, 41, 42, 62, 72, 82, 91, 101, 104, 106, 106, 106, 106, 107, 124, 131, 135, 138, 144, 148, 153, 159, 174, 177, 185, 202, 218, 228, 246, 255, 263]
          }
      }
  */
  var month_comparison = JSON.parse(document.getElementById('month_comparison').textContent);

  var months = Object.keys(month_comparison);
  var colors = ['#191970', '#1e90ff', '#87cefa', '#ace5ee' ];

  var line_chart_data = {};
  line_chart_data['datasets'] = [];
  for (month in months) {
    line_chart_data['datasets'].push(
      {
        label: months[month],
        data: month_comparison[months[month]]['tip_amount'],
        fill:false,
        tension: 0.2,
        borderColor: colors[month],
      }
    );
  }

  var date_labels = [];
  for (var i = 1; i <= 31; i++) {
    date_labels.push(i);
  }
  line_chart_data['labels']  = date_labels;

  var lineChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    pointHitRadius:15,
    pointRadius:4,
    title: {
        display: true,
        text: "Amount of Tips per day VS Previous Months"
    },
    legend: {
      position: "top"
    },
  };

  var lineChartConfig = {
    type: "line",
    data: line_chart_data,
    options: lineChartOptions
  };

  var lineChart = new Chart(
    document.getElementById('month_comparison_chart'),
    lineChartConfig
  );


  /*
  Utilizes the same data set as 
  var month_comparison = JSON.parse(document.getElementById('month_comparison').textContent);
  But instead makes a line chart comparing accumulated value per day vs the previous months

  */
  var value_colors = ['#933d41', '#fc6c85', '#ffb6c1', '#ffe4e1']

  var line_chart_data_value = {};
  line_chart_data_value['datasets'] = [];
  for (month in months) {
    line_chart_data_value['datasets'].push(
      {
        label: months[month],
        data: month_comparison[months[month]]['tip_value'],
        fill:false,
        tension: 0.2,
        borderColor: value_colors[month],
      }
    );
  }

  var date_labels = [];
  for (var i = 1; i <= 31; i++) {
    date_labels.push(i);
  }
  line_chart_data_value['labels']  = date_labels;

  var lineChartOptionsValue = {
    responsive: true,
    maintainAspectRatio: false,
    pointHitRadius:15,
    pointRadius:4,
    title: {
        display: true,
        text: "Value of Tips (USD) per day VS Previous Months"
    },
    legend: {
      position: "top"
    },
  };

  var lineChartConfigValue = {
    type: "line",
    data: line_chart_data_value,
    options: lineChartOptionsValue
  };

  var lineChartValue = new Chart(
    document.getElementById('month_comparison_chart_value'),
    lineChartConfigValue
  );


  /*
  Utilizes the same data set as 
  var month_comparison = JSON.parse(document.getElementById('month_comparison').textContent);
  But instead makes a line chart comparing Claimed Tips per day (first time users) vs the previous months

  */
  var value_colors = ['#1e4d2b', '#228b22', '#93c572', '#d0f0c0']

  var line_chart_data_claimed = {};
  line_chart_data_claimed['datasets'] = [];
  for (month in months) {
    line_chart_data_claimed['datasets'].push(
      {
        label: months[month],
        data: month_comparison[months[month]]['claimed_tips'],
        fill:false,
        tension: 0.2,
        borderColor: value_colors[month],
      }
    );
  }

  var date_labels = [];
  for (var i = 1; i <= 31; i++) {
    date_labels.push(i);
  }
  line_chart_data_claimed['labels']  = date_labels;

  var lineChartOptionsClaimed = {
    responsive: true,
    maintainAspectRatio: false,
    pointHitRadius:15,
    pointRadius:4,
    title: {
        display: true,
        text: "Claimed Tips (first time users) per day VS Previous Months"
    },
    legend: {
      position: "top"
    },
  };

  var lineChartConfigClaimed = {
    type: "line",
    data: line_chart_data_claimed,
    options: lineChartOptionsClaimed
  };

  var lineChartClaimed = new Chart(
    document.getElementById('month_comparison_chart_claimed'),
    lineChartConfigClaimed
  );
  
}catch(e){
  console.log("MONTH Charts don't load on ALL page");
  console.log(e);
}



/* 



What is this? Pop up Modal  



*/
// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal 
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}