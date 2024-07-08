$(document).ready(function() {
    
    var url_active = window.location.href;
    
    $('.nav-link').filter(function () {
        return this.href == url_active;
    }).addClass('active');
});