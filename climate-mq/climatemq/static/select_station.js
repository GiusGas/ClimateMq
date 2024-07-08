const apiUrl = '/api/datas/?station__id=';
var station__id;

$(document).ready(function() {  
    console.log($('.form-select option'))
    $('.form-select').change(function(){
        //window.location.href = window.location.href.replace(/\/[^\/]*$/, '/'+this.value)
        station__id = this.value;
        fetch(apiUrl+this.value)
            .then(response => {
              if (!response.ok) {
                throw new Error('Network response was not ok');
              }
              return response.json();
            })
            .then(datas => {
              console.log(datas);
              var $tbody = $('.table').find('tbody')
              $.each(datas.results, function(i, data) {
                var $tr = $('<tr>').append(
                    $('<th scope="row">').text(data.id),
                    $('<td>').text(data.value),
                    $('<td>').text(data.unit_symbol),
                    $('<td>').text(data.variable_name)
                ).append('</tr>');
                $tbody.append($tr)
                console.log($tr.html())
              })
              console.log($tbody.html())
            })
            .catch(error => {
              console.error('Error:', error);
            });
    });
    $.each('.pagination .page-item').click(function(){
        //window.location.href = window.location.href.replace(/\/[^\/]*$/, '/'+this.value)
        fetch(apiUrl+station__id+'&page='+$('.page-link').text())
            .then(response => {
              if (!response.ok) {
                throw new Error('Network response was not ok');
              }
              return response.json();
            })
            .then(datas => {
              console.log(datas);
              var $tbody = $('.table').find('tbody')
              $.each(datas.results, function(i, data) {
                var $tr = $('<tr>').append(
                    $('<th scope="row">').text(data.id),
                    $('<td>').text(data.value),
                    $('<td>').text(data.unit_symbol),
                    $('<td>').text(data.variable_name)
                ).append('</tr>');
                $tbody.append($tr)
                console.log($tr.html())
              })
              console.log($tbody.html())
            })
            .catch(error => {
              console.error('Error:', error);
            });
    });
});