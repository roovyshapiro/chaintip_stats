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
    document.getElementById("minutes_input").value = refresh_minutes;
    document.getElementById("checkbox_autoupdate").checked = checkbox_status_bool;
    //If the checkbox is already clicked when the page reloads
    if (checkbox_status_bool){
        document.getElementById("auto_update_label").innerHTML = 'Auto Refresh: ' + refresh_seconds;
        checkbox_click();
    }
    //Put in today's date into the date selector unless a date has been chosen already
    if (localStorage.getItem("selected_date") == null){
        var today = new Date();
        var today_date = `${today.getFullYear()}-${today.getMonth() + 1}-${today.getDate()}`;
        document.getElementById("date_start").value = today_date;
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
    if (refresh_minutes == '' || refresh_minutes == null){
        document.getElementById("minutes_input").value = 15;
        update_refresh_time();
    }
    if (checkbox_status == true){
        countdown_timer = setTimeout(function() {
            location.reload();
        }, refresh_seconds * 1000);
        countdown_update();
    } else {
        clearTimeout(countdown_timer);
        clearInterval(countdown_update_label_timer);
        refresh_minutes = document.getElementById("minutes_input").value;
        refresh_seconds = refresh_minutes * 60; 
        document.getElementById("auto_update_label").innerHTML = 'Auto Refresh';

    }
}

//WHEN the number input field is changed
function update_refresh_time() {
    refresh_minutes = document.getElementById("minutes_input").value;
    refresh_seconds = refresh_minutes * 60; 
    localStorage.setItem("refresh_seconds", refresh_seconds);
    localStorage.setItem("refresh_minutes", refresh_minutes);
    clearTimeout(countdown_timer);
    clearInterval(countdown_update_label_timer);
    checkbox_click();
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
        document.getElementById("auto_update_label").innerHTML = 'Auto Refresh: ' + refresh_seconds;
    }, 1000);
}

//When the submit button is clicked on the Dashboard, the 
//date and group are saved to localstorage so it can be retrieved
//after the page is reloaded.
function save_date(){
    selected_date = document.getElementById('date_start').value;
    localStorage.setItem("selected_date", selected_date);
    console.log(localStorage);
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
        if(chosen_date.getMonth() < max_month.getMonth()  || chosen_date.getMonth() == max_month.getMonth()){
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
var tips_per_day = JSON.parse(document.getElementById('all_stats_tip_per_day').textContent);

var keys = Object.keys(tips_per_day);
var values = Object.values(tips_per_day);

const labels = keys;
const data = {
  labels: labels,
  datasets: [{
    label: 'Tips Per Day',
    data: values,
    backgroundColor:'rgba(153, 102, 255, 0.2)',
    borderColor: 'rgb(153, 102, 255)',
    hoverBackgroundColor:'rgba(255, 205, 86, 0.2)',
    hoverBorderColor:'rgb(255, 205, 86)',
    borderWidth: 1
  }]
};

const config = {
    type: 'bar',
    data: data,
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    },
  };

var myChart = new Chart(
    document.getElementById('tip_per_day'),
    config
  );

/* Value per Day instead of tip amount per day */

var value_per_day = JSON.parse(document.getElementById('all_stats_value_per_day').textContent);

var value_keys = Object.keys(value_per_day);
var value_values = Object.values(value_per_day);

//Round each item in the fiat_value list to 2 decimal places
var x = 0;
var len = value_values.length
while(x < len){ 
    value_values[x] = value_values[x].toFixed(2); 
    x++
}

const value_labels = value_keys;
const value_data = {
  labels: labels,
  datasets: [{
    label: 'USD Tipped per Day',
    data: value_values,
    backgroundColor:'rgba(153, 102, 255, 0.2)',
    borderColor: 'rgb(153, 102, 255)',
    hoverBackgroundColor:'rgba(255, 205, 86, 0.2)',
    hoverBorderColor:'rgb(255, 205, 86)',
    borderWidth: 1
  }]
};

const value_config = {
    type: 'bar',
    data: value_data,
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    },
  };

var myValueChart = new Chart(
    document.getElementById('value_per_day'),
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
          backgroundColor: ["#ad84ff","#e8c3b9","#c45850"],
          data: tcr_values
        }
      ]
    },
    options: {
      title: {
        display: true,
        text: 'Claimed Tips'
      }
    }
});


/*

CHARTS FOR MONTH DATA


Rendering a bar chart of all tips per day using ChartsJS
https://docs.djangoproject.com/en/3.1/ref/templates/builtins/#json-script
https://www.chartjs.org/docs/master/samples/bar/vertical.html
*/
var month_tips_per_day = JSON.parse(document.getElementById('month_stats_tip_per_day').textContent);

var month_keys = Object.keys(month_tips_per_day);
var month_values = Object.values(month_tips_per_day);

const month_labels = month_keys;
const month_data = {
  labels: month_labels,
  datasets: [{
    label: 'Tips Per Day',
    data: month_values,
    backgroundColor:'rgba(153, 102, 255, 0.2)',
    borderColor: 'rgb(153, 102, 255)',
    hoverBackgroundColor:'rgba(255, 205, 86, 0.2)',
    hoverBorderColor:'rgb(255, 205, 86)',
    borderWidth: 1
  }]
};

const month_config = {
    type: 'bar',
    data: month_data,
    options: {
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

const month_value_labels = month_value_keys;
const month_value_data = {
  labels: month_value_labels,
  datasets: [{
    label: 'USD Tipped per Day',
    data: value_values,
    backgroundColor:'rgba(153, 102, 255, 0.2)',
    borderColor: 'rgb(153, 102, 255)',
    hoverBackgroundColor:'rgba(255, 205, 86, 0.2)',
    hoverBorderColor:'rgb(255, 205, 86)',
    borderWidth: 1
  }]
};

const month_value_config = {
    type: 'bar',
    data: month_value_data,
    options: {
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
          backgroundColor: ["#ad84ff","#e8c3b9","#c45850"],
          data: month_tcr_values
        }
      ]
    },
    options: {
      title: {
        display: true,
        text: 'Claimed Tips'
      }
    }
});


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

/* Show Month / All Buttons */
// Currently only shows one at a time
/*
function showMonth() {
  var x = document.getElementById("all_month_data_div");
  var y = document.getElementById("all_data_div");
  if (x.style.display === "none") {
    x.style.display = "block";
    y.style.display = "none";
  } else {
    y.style.display = "block";
    x.style.display = "none";
  }
}

function showAll() {
  var y = document.getElementById("all_data_div");
  var x = document.getElementById("all_month_data_div");
  if (y.style.display === "none") {
    x.style.display = "none";
    y.style.display = "block";
  } else {
    y.style.display = "none";
    x.style.display = "block";
  }
}
*/

function showMonth() {
  var x = document.getElementById("all_month_data_div");
  var y = document.getElementById("all_data_div");
  var month_btn = document.getElementById("show_month_button");
  var all_btn = document.getElementById("show_all_button");

  x.style.display = "block";
  y.style.display = "none";
  month_btn.style.display="none";
  all_btn.style.display="block";
}

function showAll() {
  var y = document.getElementById("all_data_div");
  var x = document.getElementById("all_month_data_div");
  var all_btn = document.getElementById("show_all_button");
  var month_btn = document.getElementById("show_month_button");

    x.style.display = "none";
    y.style.display = "block";
    all_btn.style.display="none";
    month_btn.style.display="block";


}