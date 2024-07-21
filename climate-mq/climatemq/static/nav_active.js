const absolute_url = "http://localhost:8080"
$(document).ready(function() {
    
    var url_active = absolute_url + window.location.pathname;
    
    $('.nav-link').filter(function () {
        return this.href == url_active;
    }).addClass('active');
});