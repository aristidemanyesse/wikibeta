$(function() {
    $('.input-group').datepicker({
        format:"dd/mm/yyyy",
        todayBtn: "linked",
        keyboardNavigation: false,
        forceParse: false,
        calendarWeeks: true,
        autoclose: true
    })



    $("input").change(function() {
        var mydate = $('.input-group').datepicker("getDate")
        month = mydate.getUTCMonth()+1

        localStorage.setItem("date", mydate)
        window.location.href = "/fixtures/" + mydate.getUTCFullYear() + "/" + month + "/" + mydate.getUTCDate() + "/" 
    });

})