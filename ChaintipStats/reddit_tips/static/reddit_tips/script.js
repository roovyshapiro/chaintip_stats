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

  /* */