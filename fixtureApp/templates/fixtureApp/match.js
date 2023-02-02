$(document).ready(function () {

    $('input[name=domicile]').on("ifChecked", function(){
        $("tr.not_domicile").hide(300)
    });

    $('input[name=domicile]').on("ifUnchecked", function(){
        $("tr.not_domicile").show(300)
    });


    $('input[name=exterieur]').on("ifChecked", function(){
        $("tr.not_exterieur").hide(300)
    });

    $('input[name=exterieur]').on("ifUnchecked", function(){
        $("tr.not_exterieur").show(300)
    });


});