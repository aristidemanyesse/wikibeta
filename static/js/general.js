$(document).ready(function () {

    $('.i-checks').iCheck({
        checkboxClass: 'icheckbox_square-green',
        radioClass: 'iradio_square-green',
    });







    // Recherches
    $("#form-cote").submit(function (e) {
        domicile = $(this).find("input[name=domicile]").val();
        nul = $(this).find("input[name=nul]").val();
        exterieur = $(this).find("input[name=exterieur]").val();
        window.location.href = "/stats/rechercher/cote/"+domicile+"/"+exterieur+"/"+nul+"/";
        return false
    })


    $("#form-ppg").submit(function (e) {
        domicile = $(this).find("input[name=domicile]").val();
        exterieur = $(this).find("input[name=exterieur]").val();
        window.location.href = "/stats/rechercher/cote/"+domicile+"/"+exterieur+"/";

        return false
    })
});