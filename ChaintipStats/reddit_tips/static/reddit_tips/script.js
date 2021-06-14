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