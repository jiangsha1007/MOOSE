$(function () {
    var date = $('#simulation_date').val().split(',');
    var simulation_type = eval('(' + $('#simulation_type').val() + ')');
    var simulation_user = eval('(' + $('#simulation_user').val() + ')');
    var simulation_user_name = eval('(' + $('#simulation_user_name').val() + ')');

    var simulation_result = eval('(' + $('#simulation_result').val() + ')');
    for(var i=0; i< simulation_user.length; i++){
        var dom_simulation = document.getElementById("container_simulation_"+simulation_user[i]);
        var myChart_simulation = echarts.init(dom_simulation);
        $("#user_"+simulation_user[i]).text(simulation_user_name[i])
        draw_sentiment_type(myChart_simulation, simulation_result[i],simulation_type);
    }



    window.onresize = function () {

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
        boundaryGap: true,
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
}


function draw_sentiment_type(myChart, data,type) {
    myChart.setOption(option, true);
    myChart.setOption({
        legend: {
            data: type,
            textStyle:{//图例文字的样式
                color:'#fff',
                fontSize:14
            }
        },
        dataset: {
            dimensions: ['date', 'IssuesEvent', 'PullRequestEvent', 'IssueCommentEvent','CommitCommentEvent','PullRequestReviewCommentEvent'],
            source:data
        },
        xAxis: {
            type: 'category',
        },
        series:[
            {
                type: 'bar',
                stack: '总量',
            },
            {
                type: 'bar',
                stack: '总量',
            },
            {
                type: 'bar',
                stack: '总量',
            },
            {
                type: 'bar',
                stack: '总量',
            },
            {
                type: 'bar',
                stack: '总量',
            },
        ]
    });
}
