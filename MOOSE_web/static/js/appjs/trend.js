$(function () {
    /*commit*/
    var dom_commit = document.getElementById("container_commit");
    var myChart_commit = echarts.init(dom_commit, "shine");
    var date_commit = $('#line_commit_arr').val().split(',');
    var data_commit = $('#line_commit_data').val().split(',');
    draw_commit(myChart_commit, date_commit, data_commit);

    /*issue*/
    var dom_issue = document.getElementById("container_issue");
    var myChart_issue = echarts.init(dom_issue, "shine");
    var date_issue = $('#line_issue_arr').val().split(',');
    var data_issue = $('#line_issue_data').val().split(',');
    var data_issue_close = $('#line_issue_close_data').val().split(',');
    draw_issue(myChart_issue, date_issue, data_issue, data_issue_close);

    var dom_pull = document.getElementById("container_pull");
    var myChart_pull = echarts.init(dom_pull, "shine");
    var date_pull = $('#line_pull_arr').val().split(',');
    var data_pull = $('#line_pull_data').val().split(',');
    var data_pull_close = $('#line_pull_close_data').val().split(',');
    draw_pull(myChart_pull, date_pull, data_pull, data_pull_close);

     var dom_hour = document.getElementById("container_hour");
     var myChart_hour = echarts.init(dom_hour);
     var data_arr = $('#commit_hourday').val().split(',');
     draw_hour(myChart_hour, data_arr)

    window.onresize = function () {
        myChart_commit.resize();
        myChart_issue.resize();
        myChart_hour.resize();
        myChart_pull.resize()
    }


})
var option = {
    tooltip: {
            trigger: 'axis',
            position: function (pt) {
                return [pt[0], '10%'];
            }
        },
    xAxis: {
        type: 'category',
        boundaryGap: false,
        axisLabel: {
            show: true,
            textStyle: {
                color: '#fff',
                fontSize:'12'
            }
        },
        axisLine:{
            lineStyle:{
                color:'rgba(255,255,255,0.1)',
                width:1,//这里是为了突出显示加上的		                        }
            }
        },
        splitLine:{
            show:true,
            lineStyle:{
                color:'rgba(255,255,255,0.1)',
            }
        }
    },
    yAxis: {
        type: 'value',
        boundaryGap: [0, '10%'],
        axisLabel: {
            show: true,
            textStyle: {
                color: '#fff',
                fontSize:'12'
            }
        },
        axisLine:{
            lineStyle:{
                color:'rgba(255,255,255,0.1)',
                width:1,//这里是为了突出显示加上的		                        }
            }
        },
        splitLine:{
            show:true,
            lineStyle:{
                color:'rgba(255,255,255,0.1)',
            }
        }
    },
    dataZoom: [{
        type: 'inside',
        start: 0,
        end: 100
    }, {
        start: 0,
        end: 100,
        handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
        handleSize: '80%',
        handleStyle: {
            color: '#fff',
            shadowBlur: 3,
            shadowColor: 'rgba(0, 0, 0, 0.6)',
            shadowOffsetX: 2,
            shadowOffsetY: 2
        },
        textStyle:{
            color:'#fff',
        },
    }],
    series: [
        {
            smooth:false,
            symbol: 'none',
            sampling: 'average',
        },
        {
            smooth:false,
            symbol: 'none',
            sampling: 'average',
        }
    ]
}


function draw_commit(myChart, date, data) {
    myChart.setOption(option, true);
    myChart.setOption({
        xAxis: {
            data:date
        },
        series:[
            {
                type:'line',
                name:'new commit count',
                data: data
            }
        ]
    });
}

function draw_issue(myChart, date, data, data_close){
    myChart.setOption(option, true);
    myChart.setOption({
        xAxis: {
            data:date
        },
        series:[
            {
                type:'line',
                name:'new issue count',
                data: data
            },
            {
                type:'line',
                name:'close issue count',
                data: data_close
            },

        ]
    });
}

function draw_pull(myChart, date, data_close) {
    myChart.setOption(option, true);
    myChart.setOption({
        xAxis: {
            data:date
        },
        series:[
            {
                type:'line',
                name:'new pull request count',
                data: data
            },
            {
                type:'line',
                name:'merged pull request count',
                data: data_close
            }
        ]
    });
}

function draw_hour(myChart, data_arr) {
    var hours = ['12a', '1a', '2a', '3a', '4a', '5a', '6a',
        '7a', '8a', '9a','10a','11a',
        '12p', '1p', '2p', '3p', '4p', '5p',
        '6p', '7p', '8p', '9p', '10p', '11p'];
    var days = ['Saturday', 'Friday', 'Thursday',
        'Wednesday', 'Tuesday', 'Monday', 'Sunday'];
    var data = new Array()
    var max = 0
    for(var i =0; i<data_arr.length; i++) {
        data[i] = new Array();
        var data_temp = data_arr[i].split('-');
        for (var j = 0; j < 3; j++) {
            data[i][j] = parseInt(data_temp[j].replace('\'', ''));
            if(j==2){
                if(data[i][j]>max){
                    max = data[i][j]
                }
            }
        }
    }

    data = data.map(function (item) {
        return [item[1], item[0], item[2]];
    });

    option = {
        tooltip: {
            position: 'top'
        },
        animation: false,
        grid: {
            height: '50%',
            top: '10%'
        },
        xAxis: {
            type: 'category',
            data: hours,
            splitArea: {
                show: true
            },
            axisLabel: {
                show: true,
                textStyle: {
                    color: '#fff',
                    fontSize:'12'
                }
            },
            axisLine:{
                lineStyle:{
                    color:'rgba(255,255,255,0.1)',
                    width:1,//这里是为了突出显示加上的		                        }
                }
            },
        },
        yAxis: {
            type: 'category',
            data: days,
            splitArea: {
                show: true
            },
            axisLabel: {
                show: true,
                textStyle: {
                    color: '#fff',
                    fontSize:'12'
                }
            },
            axisLine:{
                lineStyle:{
                    color:'rgba(255,255,255,0.1)',
                    width:1,//这里是为了突出显示加上的		                        }
                }
            },
        },
        visualMap: {
            min: 0,
            max: max,
            calculable: true,
            orient: 'horizontal',
            left: 'center',
            bottom: '1%',
            textStyle: {
                color: '#fff',
            },
        },
        series: [{
            name: 'Punch Card',
            type: 'heatmap',
            data: data,
            label: {
                show: true
            },
            emphasis: {
                itemStyle: {
                    shadowBlur: 10,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }]
    };
    myChart.setOption(option, true);
}