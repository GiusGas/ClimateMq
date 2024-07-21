const url = '/api/chart/get_chart_data/'

$(document).ready( function () {
    $.getJSON(url).done(function(response) {
        console.log(response)
        const ctx = document.getElementById('myChart').getContext('2d');

        const myChart = new Chart(ctx, {
          type: 'line', // or 'bar', 'pie', etc.
          data: {
            labels: response.labels,
            datasets: response.dataset
          },
          options: {
              scales: {
                  y: {
                      beginAtZero: true
                  }
              }
          }
        });   
    });
});