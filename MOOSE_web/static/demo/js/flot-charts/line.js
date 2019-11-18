'use strict';

$(document).ready(function(){
    var line_commit_data = $('#line_commit_data').val();
    var line_commit_arr = $('#line_commit_arr').val();
    var line_commit_data_arr = line_commit_data.split(',');
    var line_commit_arr_arr = line_commit_arr.split(',');
    var d1 = new Array();
    var d2 = new Array();
    for(var i =0; i<line_commit_data_arr.length; i++ ) {

        d1[i] = new Array();
        d1[i][0] = i;
        d1[i][1] = line_commit_data_arr[i];
        d2[i] = new Array();
        d2[i][0] = i;
        d2[i][1] = line_commit_arr_arr[i];
    }
    // Chart Data
    var lineChartData = [
        {
            label: 'All Repos',
            data: d1,
            color: '#fff'
        },
    ];

    // Chart Options
    var lineChartOptions = {
        series: {
            lines: {
                show: true,
                barWidth: 0.05,
                fill: 0
            }
        },
        shadowSize: 0.1,
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

        xaxis:{
            ticks:d2,
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
            container: '.flot-chart-legends--line',
            backgroundOpacity: 0.5,
            noColumns: 0,
            lineWidth: 0,
            labelBoxBorderColor: 'rgba(255,255,255,0)'
        }
    };

    // Create chart
    if ($('.flot-line')[0]) {
        $.plot($('.flot-line'), lineChartData, lineChartOptions);
    }
});
