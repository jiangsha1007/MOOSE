$(function () {
    /*sentiment*/
    var dom_sentiment = document.getElementById("container_sentiment");
    var myChart_sentiment = echarts.init(dom_sentiment);
    var date = $('#sentiment_date').val().split(',');
    var data_pos = $('#sentiment_pos').val().split(',');
    var data_neg = $('#sentiment_neg').val().split(',');
    var data_neu = $('#sentiment_neu').val().split(',');
    var data_agv = $('#sentiment_agv').val().split(',');
    draw_sentiment(myChart_sentiment, date, data_pos, data_neg, data_neu, data_agv);

    /*debate*/
    var dom_debate = document.getElementById("container_sentiment_debate");
    var myChart_debate = echarts.init(dom_debate, "shine");
    var date_sentiment_debate = $('#sentiment_type_date').val().split(',');
    var data_sentiment_debate = $('#sentiment_type_debate').val().split(',');
    var data_sentiment_comment_id = $('#sentiment_type_comment_id').val().split(',');
    var data_sentiment_debate_arr = []
    for(var i=0; i<data_sentiment_debate.length; i++){
        data_sentiment_debate_arr.push({value:data_sentiment_debate[i],"comment_id":data_sentiment_comment_id[i]})
    }
    draw_sentiment_type(myChart_debate, date_sentiment_debate, data_sentiment_debate_arr,'debate count');

     /*bug*/
    var dom_bug = document.getElementById("container_sentiment_bug");
    var myChart_bug = echarts.init(dom_bug, "shine");
    var date_sentiment_bug = $('#sentiment_type_date').val().split(',');
    var data_sentiment_bug = $('#sentiment_type_bug').val().split(',');
    var data_sentiment_bug_arr = []
    for(var i=0;i<data_sentiment_bug.length;i++){
        data_sentiment_bug_arr.push({value:data_sentiment_bug[i],"comment_id":data_sentiment_comment_id[i]})
    }
    draw_sentiment_type(myChart_bug, date_sentiment_bug, data_sentiment_bug_arr,'bug count');

     /*confuse*/
    var dom_confuse = document.getElementById("container_sentiment_confuse");
    var myChart_confuse = echarts.init(dom_confuse, "shine");
    var date_sentiment_confuse = $('#sentiment_type_date').val().split(',');
    var data_sentiment_confuse = $('#sentiment_type_confuse').val().split(',');
    var data_sentiment_confuse_arr = []
    for(i=0;i<data_sentiment_confuse.length;i++){
        data_sentiment_confuse_arr.push({value:data_sentiment_confuse[i],"comment_id":data_sentiment_comment_id[i]})
    }
    draw_sentiment_type(myChart_confuse, date_sentiment_confuse, data_sentiment_confuse_arr,'confuse count');

     /*apologize*/
    var dom_apologize = document.getElementById("container_sentiment_apologize");
    var myChart_apologize = echarts.init(dom_apologize, "shine");
    var date_sentiment_apologize = $('#sentiment_type_date').val().split(',');
    var data_sentiment_apologize = $('#sentiment_type_apologize').val().split(',');
    var data_sentiment_apologize_arr = []
    for(i=0;i<data_sentiment_apologize.length;i++){
        data_sentiment_apologize_arr.push({value:data_sentiment_apologize[i],"comment_id":data_sentiment_comment_id[i]})
    }
    draw_sentiment_type(myChart_apologize, date_sentiment_apologize, data_sentiment_apologize_arr,'apologize count');

    /*Third Part*/
    var dom_third_party = document.getElementById("container_sentiment_third_party");
    var myChart_third_party = echarts.init(dom_third_party, "shine");
    var date_sentiment_third_party = $('#sentiment_type_date').val().split(',');
    var data_sentiment_third_party = $('#sentiment_type_third_party').val().split(',');
    var data_sentiment_third_party_arr = []
    for(i=0;i<data_sentiment_third_party.length;i++){
        data_sentiment_third_party_arr.push({value:data_sentiment_third_party[i],"comment_id":data_sentiment_comment_id[i]})
    }
    draw_sentiment_type(myChart_third_party, date_sentiment_third_party, data_sentiment_third_party_arr,'third party count');

    /*Doc Standard*/
    var dom_doc_standard = document.getElementById("container_sentiment_doc_standard");
    var myChart_doc_standard = echarts.init(dom_doc_standard, "shine");
    var date_sentiment_doc_standard = $('#sentiment_type_date').val().split(',');
    var data_sentiment_doc_standard = $('#sentiment_type_doc_standard').val().split(',');
    var data_sentiment_doc_standard_arr = []
    for(i=0;i<data_sentiment_doc_standard.length;i++){
        data_sentiment_doc_standard_arr.push({value:data_sentiment_doc_standard[i],"comment_id":data_sentiment_comment_id[i]})
    }
    draw_sentiment_type(myChart_doc_standard, date_sentiment_doc_standard, data_sentiment_doc_standard_arr,'doc standard count');


    /*work*/
    var dom_work = document.getElementById("container_sentiment_work");
    var myChart_work = echarts.init(dom_work, "shine");
    var date_sentiment_work = $('#sentiment_type_date').val().split(',');
    var data_sentiment_work = $('#sentiment_type_work').val().split(',');
    var data_sentiment_work_arr = []
    for(i=0;i<data_sentiment_work.length;i++){
        data_sentiment_work_arr.push({value:data_sentiment_work[i],"comment_id":data_sentiment_comment_id[i]})
    }
    draw_sentiment_type(myChart_work, date_sentiment_work, data_sentiment_work_arr,'work count');


    window.onresize = function () {
        myChart_sentiment.resize();
        myChart_debate.resize();
        myChart_bug.resize();
        myChart_confuse.resize();
        myChart_apologize.resize();
        myChart_third_party.resize();
        myChart_doc_standard.resize();
        myChart_work.resize();
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

function draw_sentiment(myChart, date, data_pos, data_neg, data_neu, data_agv){
    var option = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross',
                crossStyle: {
                    color: '#fff'
                }
            }
        },
        legend: {
            data:['positive','negative','neutrality'],
            textStyle:{//图例文字的样式
                color:'#fff',
                fontSize:16
            }
        },
        xAxis: [
            {
                type: 'category',
                data: date,
                axisPointer: {
                    type: 'shadow'
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
                splitLine:{
                    show:true,
                    lineStyle:{
                        color:'rgba(255,255,255,0.1)',
                    }
                }
            }
        ],
        yAxis: [
            {
                type: 'value',
                name: 'issue comment number',
                min: 0,
                boundaryGap: [0, '10%'],
                axisLabel: {
                    show: true,
                    textStyle: {
                        color: '#fff',
                        fontSize:'12'
                }},
                nameTextStyle:{//图例文字的样式
                    color:'#fff',
                    fontSize:12
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
            {
                type: 'value',
                name: 'Emotion degree',
                min: -1,
                interval: 1,
                axisLabel: {
                    show: true,
                    textStyle: {
                        color: '#fff',
                        fontSize:'12'
                }},
                nameTextStyle:{//图例文字的样式
                    color:'#fff',
                    fontSize:12
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
                },

            }
        ],
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
            name:'positive',
            type:'bar',
            data:data_pos,
            itemStyle:{ normal:{ color:'#1CDDB1' } },
        },
        {
            name:'negative',
            type:'bar',
            data:data_neg,
            itemStyle:{ normal:{ color:'#bb414d' } },
        },
        {
            name:'neutrality',
            type:'bar',
            data:data_neu,
            itemStyle:{ normal:{ color:'#ffffff' } },
        },
        {
            name:'Emotion degree',
            type:'line',
            yAxisIndex: 1,
            data:data_agv,
            itemStyle:{ normal:{ color:'#ffbf00' } },
            markArea:{
                data:[[
                    {
                        yAxis: 0,
                        name:'positive area',
                        itemStyle:{ //控制当前区域样式
                           color:'rgba(28, 221, 177,0.3)'
                       }
                    },{
                        yAxis:1
                    }
                ],
                [
                    {
                        yAxis:-1
                    },
                    {
                        yAxis: 0,
                        name:'negative area',
                        itemStyle:{ //控制当前区域样式
                           color:'rgba(187, 65, 77,0.3)'
                       }

                    }
                ]]
            },
            markLine: {
                data: [
                    {
                        yAxis: 0,
                        name:'neutrality',
                        itemStyle: {
                            normal: {
                                color: '#ff3300',
                                width: 3,
                            }
                        }
                    },
                ]
            },
        }
    ]
    };
    if (option && typeof option === "object") {
    myChart.setOption(option, true);
    }
}


function draw_sentiment_type(myChart, date, data,name) {
    myChart.setOption(option, true);
    myChart.setOption({
        xAxis: {
            data:date
        },
        series:[
            {
                type:'bar',
                name:name,
                data: data

            }
        ]
    });
    myChart.on('click', function (params) {
        //alert(params.dataIndex)
        $.ajax({
            url: '/display_comment/',
            type: 'POST',
            data: {
                comment_id:params.data.comment_id
            },
            success: function(data) {
                $("#modal-comment").modal();
                //$("#dabate_count").text(data_sentiment_debate[params.dataIndex])
                for(var i=0;i< data.length;i++) {
                    html = "<hr>" +
                    "<div class=\"row\"> " +
                    "<div class=\"col-md-12\"> " +
                    "<div class=\"card\"> " +
                    "<div class=\"card-header\" style='margin-bottom: 0px'><span style=\"color: #ff0000\" >"+data[i].user_name+"@"+data[i].create_time+ "</span>" +
                    "<div style=\"float: right\"><span style=\"color: #ffff00\" >"+data[i].oss_name+"&nbsp;issue#"+data[i].issue_number+"</span></div>"+
                    "</div> " +
                    "<div class=\"card-body\"> " +
                    "<p class=\"card-text\" style='font-size: 12pt'>"+data[i].body+"</p> " +
                    "</div> " +
                    "</div> " +
                    "</div> " +
                    "</div>"
                    $("#comment_list_body").append(html)
                }

            }
        })
        //alert("单击了"+params.name+"柱状图"+option.series[params.seriesIndex].ids[param.dataIndex]);
    })
}
