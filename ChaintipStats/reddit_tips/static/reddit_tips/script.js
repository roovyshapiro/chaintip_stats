//https://datatables.net/
//Data Tables provides built in functionality such as
//sorting, filtering & choosing how many rows to load
$(document).ready( function () {
    $('table.data_table').DataTable();
} );

var value = JSON.parse(document.getElementById('all_stats').textContent);
console.log(value);
