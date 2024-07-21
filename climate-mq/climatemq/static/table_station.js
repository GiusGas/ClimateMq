const apiUrl = '/api/table_stations/?format=datatables';

$(document).ready( function () {

    $('#stationTable').css("visibility", "visible")

    let table = $('#stationTable').DataTable( {
      "serverSide": true,
      "processing": true,
      "destroy": true,
      "ajax": {
        "url": apiUrl,
      },
      columns: [
          { data: 'id', name: 'id' },
          { data: 'name', name: 'name', render: function(data, type, row, meta) {
            return `<a href="/climatemq/dashboard?selectValue=${row.id}">${data}</a>`;
            } 
          },
          { data: 'latitude', name: 'latitude' },
          { data: 'longitude', name: 'longitude' }
      ]
    });
} );
