'use strict';

$(document).ready(function(){
    var bar_lanuage_data = $('#bar_lanuage_data').val();
    var bar_lanuage_arr = $('#bar_lanuage_arr').val();
    var bar_lanuage_data_arr = bar_lanuage_data.split(',');
    var bar_lanuage_arr_arr = bar_lanuage_arr.split(',');
    var d1 = new Array();
    var d2 = new Array();
    for(var i =0; i<10; i++ ) {

        d1[i] = new Array();
        d1[i][0] = i;
        d1[i][1] = bar_lanuage_data_arr[i];
        d2[i] = new Array();
        d2[i][0] = i;
        d2[i][1] = bar_lanuage_arr_arr[i];
    }
     var arr = d2;

    // Chart Data
    var barChartData = [
        {
            label: 'Language',
            data: d1,
            bars: {
                order: 0,
                fillColor: '#fff'
            },
            color: '#fff'
        },

    ];


    // Chart Options
    var barChartOptions = {
        series: {
            bars: {
                show: true,
                barWidth: 0.075,
                fill: 0.1,
                lineWidth: 0
            }
        },
        grid : {
            borderWidth: 1,
            borderColor: 'rgba(255,255,255,0.1)',
            show : true,
            hoverable : true,
            clickable : true
        },
        yaxis: {
            tickColor: 'rgba(255,255,255,0.1)',
            tickDecimals: 0,
            font: {
                lineHeight: 13,
                style: 'normal',
                color: 'rgba(255,255,255,0.75)',
                size: 11
            },
            shadowSize: 0
        },
        xaxis: {
            ticks:arr,
            tickColor: 'rgba(255,255,255,0.1)',
            tickDecimals: 0,
            font: {
                lineHeight: 13,
                style: 'normal',
                color: 'rgba(255,255,255,0.75)',
                size: 11
            },
            shadowSize: 0
        },
        legend:{
            container: '.flot-chart-legends--bar',
            backgroundOpacity: 0.5,
            noColumns: 0,
            lineWidth: 0,
            labelBoxBorderColor: 'rgba(255,255,255,0)'
        }
    };

    // Create chart
    if ($('.flot-bar')[0]) {
        $.plot($('.flot-bar'), barChartData, barChartOptions);
    }
});
