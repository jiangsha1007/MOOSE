$(function () {
    var cid = $('#cid').val();
    /*score*/
    var oss_score = $('#oss_score').val();
    var oss_name = $('#oss_name').val();
    var dom_score = document.getElementById("container_score");
    var myChart_score = echarts.init(dom_score);
    draw_score(myChart_score, oss_name, oss_score);


    /*net*/
    var dom_net = document.getElementById("container_net");
    var myChart_net = echarts.init(dom_net, "shine");
    var data_categories = eval('(' +$('#net_categories').val() + ')'); ;
    var data_nodes = eval('(' +$('#net_nodes').val()+ ')') ;
    var data_links = eval('(' +$('#net_links').val() + ')');
    draw_net(myChart_net, data_categories, data_nodes, data_links);

    /*fork star pop*/
    var dom_pop = document.getElementById("container_pop");
    var myChart_pop = echarts.init(dom_pop,"shine");
    var date_pop = $('#line_pop_arr').val().split(',');
    var data_pop = $('#line_pop_data').val().split(',');
    var data_fork = $('#line_fork_data').val().split(',');
    var data_star = $('#line_star_data').val().split(',');
    draw_pop(myChart_pop, date_pop, data_pop, data_fork, data_star);

    /*sem*/
    var pop = $("#oss_popularity_sem").val();
    var ncdpr = $("#oss_ncdpr_sem").val();
    var ncdic = $("#oss_ncdic_sem").val();
    var ncdcc = $("#oss_ncdcc_sem").val();
    var ncdrc = $("#oss_ncdrc_sem").val();
    var ncdr = $("#oss_ncdr_sem").val();
    var npr = $("#oss_npr_sem").val();
    var nprc = $("#oss_nprc_sem").val();
    var prrr = $("#oss_prrr_sem").val();
    var nprrc = $("#oss_nprrc_sem").val();
    var nic = $("#oss_nic_sem").val();
    var ncd = $("#oss_ncd_sem").val();
    var ncc = $("#oss_ncc_sem").val();
    var nd = $("#oss_nd_sem").val();
    var ni = $("#oss_ni_sem").val();
    var nl = $("#oss_nl_sem").val();
    var icr = $("#oss_icr_sem").val();
    var prmr = $("#oss_prmr_sem").val();
    var myChart_sem = echarts.init(document.getElementById("container_sem"));
    draw_sem(myChart_sem, pop, ncdpr, ncdic, ncdcc, ncdrc, ncdr, npr, nprc, prrr, nprrc, nic, ncd, ncc, nd, ni, nl, icr, prmr);

    /*language*/
    var dom_language = document.getElementById("container_language");
    var myChart_language = echarts.init(dom_language,"shine");
    var data = $('#bar_language_data').val().split(',');
    var date = $('#bar_language_arr').val().split(',');
    draw_language(myChart_language, date, data);

    /*websocket*/
    var websocket;
 // 首先判断是否 支持 WebSocket  name身份标识  我当前用的 用户名，
    if('WebSocket' in window) {
        websocket = new WebSocket("ws://127.0.0.1:8000/websocketLink?id="+cid);
    } else if('MozWebSocket' in window) {
        websocket = new MozWebSocket("ws://localhost:8000/websocketLink?id="+cid);
    } else {
        websocket = new SockJS("ws://localhost:8000/websocketLink?id="+cid);
    }
    // 打开连接时    formatMsg是我自定义的消息提示
    websocket.onopen = function(event) {

    }
    ;
    // 收到消息时
    websocket.onmessage = function(event) {
        var data =JSON.parse(event.data);
        $('#moose_loc').text(data.loc);
        $('#moose_updatetime').text(data.moose_time);
        $('#moose_doc').text(data.doc);
        $('#moose_foc').text(data.foc);
        $('#moose_coc').text(data.coc);
        $('#moose_issue_count').text(data.issue_count);
        $('#moose_issue_close_count').text(data.issue_close);
        $('#moose_issue_open').text(data.issue_open);
        $('#moose_pull_count').text(data.pulls_count);
        $('#moose_pull_merged_count').text(data.pulls_merged);
        $('#moose_pull_unmerged_count').text(data.pulls_unmerged);
        $('#moose_star_count').text(data.star_count);
        $('#moose_fork_count').text(data.fork_count);
        $('#moose_popularity').text(data.popularity);
        $('#moose_issue_comment_count').text(data.issue_comment_count);
        $('#moose_pull_comment_count').text(data.pull_comment_count);
        $('#moose_review_comment_count').text(data.review_comment_count);

        $('#moose_pull_review_count').text(data.pull_review_count);
        $('#moose_issue_close_time').text(data.issue_close_time);
        $('#moose_pull_merged_time').text(data.pull_merged_time);

        $('#bar_language_data').text(data.bar_language_data);
        $('#bar_language_arr').text(data.bar_language_arr);

        $('#sentiment_date').text(data.sentiment_date);
        $('#sentiment_pos').text(data.sentiment_pos);
        $('#sentiment_neg').text(data.sentiment_neg);
        $('#sentiment_neu').text(data.sentiment_neu);
        $('#sentiment_agv').text(data.sentiment_agv);

        $('#moose_issue_closed').text(data.issue_closed);
        $('#moose_pull_merged').text(data.pull_merged);
        $('#moose_developer_core').text(data.developer_core);
        $('#moose_core_issue').text(data.core_issue);
        $('#moose_core_pull').text(data.core_pull);
        $('#moose_active_day').text(data.active_day);
        var event_html = '';

        for(var i = 0;i<data.event.length;i++){
            event_html +='<tr>';
            event_html += '<td>' + data.event[i].event_type + '</td>';
            event_html += '<td>' + data.event[i].event_name + '</td>';
            event_html += '<td>' + data.event[i].event_action + '</td>';
            event_html += '<td>' + data.event[i].event_time + '</td>';
            event_html +='</tr>';
        }

        $('#event_body').html(event_html)

    };
    // 错误时
    websocket.onerror = function(event) {
        console.log("  websocket.onerror  ");
    };
    // 断开连接时
    websocket.onclose = function(event) {

    };
        //关闭websocket连接
    $('#close_websocket').click(function () {
        if(websocket){
            websocket.close();
        }
    });
    if (websocket.readyState == WebSocket.OPEN){
        websocket.onopen();
    }
    window.onresize = function () {
        myChart_score.resize();
        myChart_sentiment.resize();
        myChart_sem.resize();
        myChart_language.resize();
        myChart_net.resize();
        myChart_pop.resize();
    }


})

function draw_score(myChart, oss_name, oss_score) {
    var oss_name_arr = oss_name.split(',');
    var oss_score_arr = oss_score.split(',');
    option = null;
    var lineStyle = {
        normal: {
            width: 1,
            opacity: 0.5
        }
    };
    var seri = new Array();
    for (var i = 0; i < oss_name_arr.length; i++) {
        seri[i] = {
            name: oss_name_arr[i], type: 'radar', lineStyle: lineStyle, data: [oss_score_arr[i].split('-')],
            symbol: 'none', itemStyle: {normal: {color: '#bb414d'}}, areaStyle: {normal: {opacity: 0.5}}
        };
    }
    option = {
        backgroundColor: 'rgba(128, 128, 128, 0.0)',
        legend: {
            bottom: 'bottom',
            data: oss_name_arr,
            itemGap: 20,
            textStyle: {
                color: '#fff',
                fontSize: 12
            },
            selectedMode: 'single',
            orient: 'horizontal',
            x: 'center',
            y: 'bottom',
            padding: [30, 0, 0, 0],
        },
        radar: {
            indicator: [
                {name: 'Develop Activity', max: 100},
                {name: 'Community Activity', max: 100},
                {name: 'Attractiveness', max: 100},
                {name: 'Develop Duration', max: 100},
                {name: 'Problem Solution', max: 100},
                {name: 'Develop Efficiency', max: 100}
            ],
            radius: 90,
            shape: 'circle',
            splitNumber: 5,
            name: {
                textStyle: {
                    color: 'rgb(255, 255, 255)'
                }
            },
            splitLine: {
                lineStyle: {
                    color: [
                        'rgba(238, 197, 102, 0.1)', 'rgba(238, 197, 102, 0.2)',
                        'rgba(238, 197, 102, 0.4)', 'rgba(238, 197, 102, 0.6)',
                        'rgba(238, 197, 102, 0.8)', 'rgba(238, 197, 102, 1)'
                    ].reverse()
                }
            },
            splitArea: {
                show: false
            },
            axisLine: {
                lineStyle: {
                    color: 'rgba(238, 197, 102, 0.5)'
                }
            }
        },
        series: seri
    };
    if (option && typeof option === "object") {
        myChart.setOption(option, true);
    }
}


function draw_sem(myChart, pop, ncdpr, ncdic, ncdcc, ncdrc, ncdr, npr, nprc, prrr, nprrc, nic, ncd, ncc, nd, ni, nl, icr, prmr) {
    var option = {
            tooltip: {
                formatter: function(param) {
                    if (param.dataType === 'edge') {
                        //return param.data.category + ': ' + param.data.target;
                        return "weight:" +param.data.target;
                    }
                    //return param.data.category + ': ' + param.data.name;
                    return param.data.category;
                }
            },
            animationDurationUpdate: 1500,
            animationEasingUpdate: 'quinticInOut',
            series: [
                {
                    type: 'graph',
                    layout: 'none',
                    symbolSize: 50,
                    roam: true,
                    label: {
                        show: true
                    },
                    edgeSymbol: ['circle', 'arrow'],
                    edgeSymbolSize: [4, 10],
                    edgeLabel: {
                        fontSize: 20
                    },
                    data: [{
                        name: "Popularity",
                        symbolSize: [100, 100],         // 关系图节点标记的大小，可以设置成诸如 10 这样单一的数字，也可以用数组分开表示宽和高，例如 [20, 10] 表示标记宽为20，高为10。
                        itemStyle: {
                            color: '#805f00'				// 关系图节点标记的颜色
                        },
                        category: pop,      // 数据项所在类目的 index。
                        x: 1150,
                        y: 150,

                    }, {
                        name: "Core Developer\nParticipation",
                        symbolSize: [100, 50],
                        itemStyle: {
                            color: '#005c99'
                        },
                        category: "Latent variables",
                        x: 600,
                        y: 100
                    }, {
                        name: "Project\nActivity",
                        symbolSize: [100, 50],
                        itemStyle: {
                            color: '#005c99'
                        },
                        category: "Latent variables",
                        x: 600,
                        y: 450
                    }, {
                        name: "Community\nVitality",
                        symbolSize: [100, 50],
                        itemStyle: {
                            color: '#005c99'
                        },
                        category: "Latent variables",
                        x: 800,
                        y: 250
                    }, {
                        name: "Development\nEfficiency",
                        symbolSize: [100, 50],
                        itemStyle: {
                            color: '#005c99'
                        },
                        category: "Latent variables",
                        x: 1150,
                        y: 350
                    }, {
                        name: "Number of Core Developer Pull Requests",
                        symbolSize: [60, 60],
                        itemStyle: {
                            color: '#bb414d'
                        },
                        category: ncdpr,
                        symbol : 'rect',
                        symbolSize : [300,20],
                        x: 200,
                        y: 40
                    }, {
                        name: "Number of Core Developer Reviews",
                        itemStyle: {
                            color: '#bb414d'
                        },
                        category: ncdr,
                        symbol : 'rect',
                        symbolSize : [300,20],
                        x: 200,
                        y: 80
                    }, {
                        name: "Number of Core Developer Issue Comments",
                        itemStyle: {
                            color: '#bb414d'
                        },
                        category: ncdic,
                        symbol : 'rect',
                        symbolSize : [300,20],
                        x: 200,
                        y: 120
                    }, {
                        name: "Number of Core Developer Commit Comments",
                        itemStyle: {
                            color: '#bb414d'
                        },
                        category: ncdcc,
                        symbol : 'rect',
                        symbolSize : [300,20],
                        x: 200,
                        y: 160
                    }, {
                        name: "Number of Core Developer Review Comments",
                        itemStyle: {
                            color: '#bb414d'
                        },
                        category: ncdrc,
                        symbol : 'rect',
                        symbolSize : [300,20],
                        x: 200,
                        y: 200

                    }, {
                        name: "Number of Pull Requests",
                        itemStyle: {
                            color: '#bb414d'
                        },
                        category: npr,
                        symbol : 'rect',
                        symbolSize : [300,20],
                        x: 200,
                        y: 300
                    }, {
                        name: "Number of Pull Request Comments",
                        itemStyle: {
                            color: '#bb414d'
                        },
                        category: nprc,
                        symbol : 'rect',
                        symbolSize : [300,20],
                        x: 200,
                        y: 340
                    }, {
                        name: "Pull Request Review Ratio",
                        itemStyle: {
                            color: '#bb414d'
                        },
                        category: prrr,
                        symbol : 'rect',
                        symbolSize : [300,20],
                        x: 200,
                        y: 380
                    },{
                        name: "Number of Pull Rquest Review Comments",
                        itemStyle: {
                            color: '#bb414d'
                        },
                        category: nprrc,
                        symbol : 'rect',
                        symbolSize : [300,20],
                        x: 200,
                        y: 420
                    },{
                        name: "Number of Issue Commits",
                        itemStyle: {
                            color: '#bb414d'
                        },
                        category: nic,
                        symbol : 'rect',
                        symbolSize : [300,20],
                        x: 200,
                        y: 460
                    },{
                        name: "Number of Core Developers",
                        itemStyle: {
                            color: '#bb414d'
                        },
                        category: ncd,
                        symbol : 'rect',
                        symbolSize : [300,20],
                        x: 200,
                        y: 500
                    },{
                        name: "Number of Developers",
                        itemStyle: {
                            color: '#bb414d'
                        },
                        category: nd,
                        symbol : 'rect',
                        symbolSize : [300,20],
                        x: 200,
                        y: 540
                    },{
                        name: "Number of Developers 1",
                        itemStyle: {
                            color: '#bb414d'
                        },
                        category: nd,
                        symbol : 'rect',
                        symbolSize : [300,20],
                    },{
                        name: "Number of Issues",
                        itemStyle: {
                            color: '#bb414d'
                        },
                        category: ni,
                        symbol : 'rect',
                        symbolSize : [160,40],
                        x: 700,
                        y: 350
                    },{
                        name: "Number of Languages",
                        itemStyle: {
                            color: '#bb414d'
                        },
                        category: nl,
                        symbol : 'rect',
                        symbolSize : [160,40],
                        x: 900,
                        y: 350
                    },{
                        name: "Number of Commit\nComments",
                        itemStyle: {
                            color: '#bb414d'
                        },
                       category: ncc,
                        symbol : 'rect',
                        symbolSize : [130,40],
                        x: 800,
                        y: 150
                    },{
                        name: "Issue Close Ratio",
                        itemStyle: {
                            color: '#bb414d'
                        },
                        category: icr,
                        symbol : 'rect',
                        symbolSize : [160,40],
                        x: 1000,
                        y: 520
                    },{
                        name: "Pull Request Merged Ratio",
                        itemStyle: {
                            color: '#bb414d'
                        },
                        category: prmr,
                        symbol : 'rect',
                        symbolSize : [180,40],
                        x: 1200,
                        y: 520
                    }],
                    links: [{
                        source: "Community\nVitality",
                        target: "Popularity",
                        symbolSize: [5, 20],
                        lineStyle: {
                            width: 5,
                        }
                    },{
                        source: "Core Developer\nParticipation",
                        target: "Project\nActivity",
                        symbolSize: [5, 20],
                        lineStyle: {
                            width: 5,
                        }
                    },{
                        source: "Core Developer\nParticipation",
                        target: "Development\nEfficiency",
                        symbolSize: [5, 20],
                        lineStyle: {
                            width: 5,
                        }
                    },
                    {
                        source: "Core Developer\nParticipation",
                        target: "Community\nVitality",
                        symbolSize: [5, 20],
                        lineStyle: {
                            width: 3,
                            type:'dotted',
                            color:"#bb414d"
                        }
                    }, {
                        source: "Core Developer\nParticipation",
                        target: "Popularity",
                        symbolSize: [5, 20],
                        lineStyle: {
                            width: 3,
                            type:'dotted',
                            color:"#bb414d"
                        }
                    },{
                        source: "Project\nActivity",
                        target: "Community\nVitality",
                        symbolSize: [5, 20],
                        lineStyle: {
                            width: 5,
                        }
                    },{
                        source: "Core Developer\nParticipation",
                        target: "Number of Core Developer Pull Requests",
                        symbolSize: [2, 20],
                        lineStyle: {
                            width: 0.756*8,
                            color:"#1CDDB1"
                        },
                        label: {
                            show: true,
                            formatter:"0.756",
                            textStyle:{//图例文字的样式
                                color:'#fff',
                                fontSize:10
                            }
                        },

                    },{
                        source: "Core Developer\nParticipation",
                        target: "Number of Core Developer Reviews",
                        symbolSize: [2, 20],
                        lineStyle: {
                            width: 0.644*8,
                            color:"rgba(28, 221, 177,0.7)"
                        },
                        label: {
                            show: true,
                            formatter:"0.644",
                            textStyle:{//图例文字的样式
                                color:'#fff',
                                fontSize:10
                            }
                        },

                    },{
                        source: "Core Developer\nParticipation",
                        target: "Number of Core Developer Issue Comments",
                        symbolSize: [2, 20],
                        lineStyle: {
                            width: 0.754*8,
                            color:"#1CDDB1"
                        },
                        label: {
                            show: true,
                            formatter:"0.754",
                            textStyle:{//图例文字的样式
                                color:'#fff',
                                fontSize:10
                            }
                        },

                    },{
                        source: "Core Developer\nParticipation",
                        target: "Number of Core Developer Commit Comments",
                        symbolSize: [2, 20],
                        lineStyle: {
                            width: 0.455*6,
                            color:'rgba(28, 221, 177,0.3)'
                        },
                        label: {
                            show: true,
                            formatter:"0.455",
                            textStyle:{//图例文字的样式
                                color:'#fff',
                                fontSize:10
                            }
                        },

                    },{
                        source: "Core Developer\nParticipation",
                        target: "Number of Core Developer Review Comments",
                        symbolSize: [2, 20],
                        lineStyle: {
                            width: 0.821*8,
                            color:"#1CDDB1"
                        },
                        label: {
                            show: true,
                            formatter:"0.821",
                            textStyle:{//图例文字的样式
                                color:'#fff',
                                fontSize:10
                            }
                        },

                    },{
                        source: "Project\nActivity",
                        target: "Number of Pull Requests",
                        symbolSize: [2, 20],
                        lineStyle: {
                            width: 0.875*8,
                            color:"#1CDDB1"
                        },
                        label: {
                            show: true,
                            formatter:"0.875",
                            textStyle:{//图例文字的样式
                                color:'#fff',
                                fontSize:10
                            }
                        },

                    },{
                        source: "Project\nActivity",
                        target: "Number of Pull Request Comments",
                        symbolSize: [2, 20],
                        lineStyle: {
                            width: 0.944*10,
                            color:"#8ef1da"
                        },
                        label: {
                            show: true,
                            formatter:"0.944",
                            textStyle:{//图例文字的样式
                                color:'#fff',
                                fontSize:10
                            }
                        },

                    },{
                        source: "Project\nActivity",
                        target: "Pull Request Review Ratio",
                        symbolSize: [2, 20],
                        lineStyle: {
                            width: 0.740*8,
                            color:"#1CDDB1"
                        },
                        label: {
                            show: true,
                            formatter:"0.740",
                            textStyle:{//图例文字的样式
                                color:'#fff',
                                fontSize:10
                            }
                        },

                    },{
                        source: "Project\nActivity",
                        target: "Number of Pull Rquest Review Comments",
                        symbolSize: [2, 20],
                        lineStyle: {
                            width: 0.830*8,
                            color:"#1CDDB1"
                        },
                        label: {
                            show: true,
                            formatter:"0.830",
                            textStyle:{//图例文字的样式
                                color:'#fff',
                                fontSize:10
                            }
                        },

                    },{
                        source: "Project\nActivity",
                        target: "Number of Issue Commits",
                        symbolSize: [2, 25],
                        lineStyle: {
                            width: 0.939*10,
                            color:"#8ef1da"
                        },
                        label: {
                            show: true,
                            formatter:"0.939",
                            textStyle:{//图例文字的样式
                                color:'#fff',
                                fontSize:10
                            }
                        },

                    },{
                        source: "Project\nActivity",
                        target: "Number of Core Developers",
                        symbolSize: [2, 25],
                        lineStyle: {
                            width: 0.930*10,
                            color:"#8ef1da"
                        },
                        label: {
                            show: true,
                            formatter:"0.930",
                            textStyle:{//图例文字的样式
                                color:'#fff',
                                fontSize:10
                            }
                        },

                    },{
                        source: "Project\nActivity",
                        target: "Number of Developers",
                        symbolSize: [2, 20],
                        lineStyle: {
                            width: 0.689*8,
                            color:"#1CDDB1"
                        },
                        label: {
                            show: true,
                            formatter:"0.689",
                            textStyle:{//图例文字的样式
                                color:'#fff',
                                fontSize:10
                            }
                        },

                    },{
                        source: "Community\nVitality",
                        target: "Number of Commit\nComments",
                        symbolSize: [2, 20],
                        lineStyle: {
                            width: 0.599*8,
                            color:"rgba(28, 221, 177,0.5)"
                        },
                        label: {
                            show: true,
                            formatter:"0.599",
                            textStyle:{//图例文字的样式
                                color:'#fff',
                                fontSize:10
                            }
                        },

                    },{
                        source: "Community\nVitality",
                        target: "Number of Issues",
                        symbolSize: [2, 20],
                        lineStyle: {
                            width: 0.772*8,
                            color:"#1CDDB1"
                        },
                        label: {
                            show: true,
                            formatter:"0.772",
                            textStyle:{//图例文字的样式
                                color:'#fff',
                                fontSize:10
                            }
                        },

                    },{
                        source: "Community\nVitality",
                        target: "Number of Languages",
                        symbolSize: [2, 20],
                        lineStyle: {
                            width: 0.594*8,
                            color:"rgba(28, 221, 177,0.5)"
                        },
                        label: {
                            show: true,
                            formatter:"0.594",
                            textStyle:{//图例文字的样式
                                color:'#fff',
                                fontSize:10
                            }
                        },

                    },{
                        source: "Development\nEfficiency",
                        target: "Pull Request Merged Ratio",
                        symbolSize: [4, 20],
                        lineStyle: {
                            width: 0.671*8,
                            color:"rgba(28, 221, 177,0.7)"
                        },
                        label: {
                            show: true,
                            formatter:"0.671",
                            textStyle:{//图例文字的样式
                                color:'#fff',
                                fontSize:10
                            }
                        },

                    },{
                        source: "Development\nEfficiency",
                        target: "Issue Close Ratio",
                        symbolSize: [2, 20],
                        lineStyle: {
                            width: 0.658*8,
                            color:"rgba(28, 221, 177,0.7)"
                        },
                        label: {
                            show: true,
                            formatter:"0.658",
                            textStyle:{//图例文字的样式
                                color:'#fff',
                                fontSize:10
                            }
                        },
                    }],
                     lineStyle: {
                        opacity: 0.9,
                        width: 2,
                    }
                }]
        }
        myChart.setOption(option)
        myChart.on('click', function (param){
            console.log('param---->', param);  // 打印出param, 可以看到里边有很多参数可以使用
        // 获取节点点击的数组序号
            var arrayIndex = param.dataIndex;
            console.log('arrayIndex---->', arrayIndex);
            console.log('name---->', param.name);
            if (param.dataType == 'node') {
                alert("点击了节点" + param.name)            }
            else {
                alert("点击了边" + param.value)            }
        });
}

function draw_language(myChart, date, data) {
    option = {
        tooltip:{},
        xAxis: {
            type: 'category',
            data:  date,
            axisLabel: {
                show: true,
                textStyle: {
                    color: '#fff',
                    fontSize:'12'
                }
            },
        },
        yAxis: {
            type: 'value',
            axisLabel: {
                show: true,
                textStyle: {
                    color: '#fff',
                    fontSize:'12'
                }
            },
        },
        series: [{
            data:  data,
            type: 'bar',
        }]
    };
    if (option && typeof option === "object") {
        myChart.setOption(option, true);
    }
}

function draw_net(myChart, data_categories, data_nodes, data_links) {
        myChart.hideLoading();
        var option = {
                title: {show:false,text: 'Collaborators'},
                tooltip: {},
                legend: [{
                    data: data_categories.map(function (a) {//显示策略
                            return a.name;
                        }),
                textStyle: { //图例文字的样式
                    color: '#fff',
                    fontSize: 12
                },
                }],
                animation: false,
                series : [
        {
            name: '',
            type: 'graph',
            layout: 'force',
            data: data_nodes,//节点数据
            links: data_links,//节点边数据
            categories: data_categories,//策略
            roam: true,//是否开启滚轮缩放和拖拽漫游，默认为false（关闭），其他有效输入为true（开启），'scale'（仅开启滚轮缩放），'move'（仅开启拖拽漫游）
            label: {
                normal: {
                    show:'false',
                    position: 'right'
                }
            },
            slient:false,//是否响应点击事件，为false的时候就是响应
            force: {
                repulsion: 200
            }
        }]

        };
        myChart.setOption(option);
}
var option_line = {
    tooltip: {
            trigger: 'axis',
            position: function (pt) {
                return [pt[0], '10%'];
            }
        },
    legend: {
            data:['popularity','fork','star'],
            textStyle:{//图例文字的样式
                color:'#fff',
                fontSize:16
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
            type: 'line',
            smooth:false,
            symbol: 'none',
            sampling: 'average',

        },
        {
            type: 'line',
            smooth:false,
            symbol: 'none',
            sampling: 'average',

        },
        {
            type: 'line',
            smooth:false,
            symbol: 'none',
            sampling: 'average',

        }
    ]
}
function draw_pop(myChart, date, data_pop, data_fork, data_star){
    myChart.setOption(option_line, true);
    myChart.setOption({
        xAxis: {
            data:date
        },
        series:[
            {
                type:'line',
                name:'popularity',
                data: data_pop
            },
            {
                type:'line',
                name:'fork',
                data: data_fork
            },
            {
                type:'line',
                name:'star',
                data: data_star
            }
        ]
    });
}