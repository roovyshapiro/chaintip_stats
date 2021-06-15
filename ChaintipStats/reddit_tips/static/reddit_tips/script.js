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

//When the submit button is clicked on the Case Dashboard, the 
//date and group are saved to localstorage so it can be retrieved
//after the page is reloaded. Sales dashboard utilizies date as well.
function save_group_date(){
    selected_group = document.getElementById("group_dropdown");
    if(selected_group){
        selected_group = document.getElementById("group_dropdown").value;
        localStorage.setItem("selected_group", selected_group);
    }

    selected_date = document.getElementById('date_start').value;
    localStorage.setItem("selected_date", selected_date);
    console.log(localStorage);
    document.getElementById("date_form").submit();

}

//This function is called when the arrows are clicked next to the timechanger
//to change the date back and forth by one day. This automatically submits the page
//as the submit function was moved to save_group_date()
function date_changer(timeframe){
    //["2020", "12", "15"]
    var chosen_date_arr = localStorage.getItem('selected_date').split('-');
    //Tue Dec 15 2020 00:00:00 GMT-0500 (Eastern Standard Time)
    chosen_date = new Date(`${chosen_date_arr[0]},${chosen_date_arr[1]},${chosen_date_arr[2]}`);

    if(timeframe=='yesterday'){
        //If its 01-01, set date to Dec 31
        chosen_date.setDate(chosen_date.getDate() - 1);
        }

    else if(timeframe=='tomorrow'){
        var today = new Date();
        //var tomorrow = new Date();
        //Don't allow user to choose a date in the future
        //end the function now so it doesn't refresh the page
        //for no reason.
        if(chosen_date > today  || chosen_date == today){
            return;
        } else{
            chosen_date.setDate(chosen_date.getDate() + 1);
        }
    }

    //1 -> 01, 3 -> 03, etc.
    var day = chosen_date.getDate();
    if(day.toString().length == 1){
        day = `0${day}`;
    }
    //1 -> 01, 3 -> 03 etc.
   var month = chosen_date.getMonth() + 1;
   if(month.toString().length == 1){
        month = `0${month}`;
    }

    new_date = `${chosen_date.getFullYear()}-${month}-${day}`;
    localStorage.setItem('selected_date', new_date);
    document.getElementById("date_start").value = new_date;
    save_group_date();
}




//********************** */

//https://datatables.net/
//Data Tables provides built in functionality such as
//sorting, filtering & choosing how many rows to load
$(document).ready( function () {
    $('table.data_table').DataTable();
} );

/*
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