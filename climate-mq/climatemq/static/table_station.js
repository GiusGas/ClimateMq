const apiUrl = '/api/datas/?station__id=';

$(document).ready( function () {

    $('.form-select').change(function(){
        //window.location.href = window.location.href.replace(/\/[^\/]*$/, '/'+this.value)
        var station__id = this.value;
        
        $('#myTable').DataTable( {
          "serverSide": true,
          "processing": true,
          "ajax": apiUrl+station__id,
          columns: [
              { data: 'id' },
              { data: 'value' },
              { data: 'unit_symbol' },
              { data: 'variable_name' }
          ]
        });
    });
} );
