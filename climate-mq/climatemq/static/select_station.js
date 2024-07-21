const apiUrl = '/api/datas/?format=datatables&station__id=';
const chart_url = '/api/chart/get_chart_data/?station__id='

let myChart;

$(document).ready( function () {

    $('.form-select').change(function(){
        //window.location.href = window.location.href.replace(/\/[^\/]*$/, '/'+this.value)
        var station__id = this.value;

        if (this.options[0] == "Select a Station") {
            this.options[0].remove()
        }

        $.getJSON(chart_url + station__id).done(function(response) {
            console.log(response)
            const ctx = document.getElementById('myChart').getContext('2d');
    
            if (myChart) {
                myChart.destroy();
            }

            myChart = new Chart(ctx, {
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

        $('#myTable').css("visibility", "visible")

        let table= $('#myTable').DataTable( {
          "serverSide": true,
          "processing": true,
          "destroy": true,
          "ajax": {
            "url": apiUrl+station__id,
          },
          columns: [
              { data: 'id', name: 'id' },
              { data: 'value', name: 'value' },
              { data: 'unit_symbol', name: 'variable__unit__symbol' },
              { data: 'variable_name', name: 'variable__name' },
              { data: 'created_at', name: 'created_at' }
          ]
        });
    });

      // Function to get URL parameters
    function getUrlParameter(name) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(name);
    }

    // Get the select value from URL parameter
    const selectValue = getUrlParameter('selectValue');
    
    // Set the value of the select element if the parameter is present
    if (selectValue) {
        const selectElement = document.getElementById('selectStation');
        selectElement.value = selectValue;
        $('#selectStation').trigger("change")
    }
} );