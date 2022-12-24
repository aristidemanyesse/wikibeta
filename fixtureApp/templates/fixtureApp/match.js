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



    var radarData = {
        labels: ["ppg", "MG", "MA", "diff", "Tirs", "Corners"],
        datasets: [
            {
                label: "uihu",
                backgroundColor: "rgba(220,220,220,0.2)",
                borderColor: "rgba(220,220,220,1)",
                data: [65, 59, 90, 81, 56, 55]
            },
            {
                label: "dshj",
                backgroundColor: "rgba(26,179,148,0.2)",
                borderColor: "rgba(26,179,148,1)",
                data: [28, 48, 19, 96, 27, 100]
            }
        ]
    };

    var radarOptions = {
        
    };

    var ctx5 = document.getElementById("radarChart").getContext("2d");
    new Chart(ctx5, {type: 'radar', data: radarData, options:radarOptions});


});