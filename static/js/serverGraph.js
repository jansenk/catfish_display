$(function () {
    $('#container').highcharts({
        chart: {
            type: 'area'
        },
        title: {
            text: 'Packets'
        },
        xAxis: {
            type: 'linear',
            title: {
                text: 'Elapsed time (ms)'
            }
        },
        yAxis: {
            title: {
                text: 'Packets'
            },
            min: 0
        },
        plotOptions: {
            spline: {
                marker: {
                    enabled: true
                }
            }
        },

        series: [{
            name: 'Total Packets',
            data: recData
        }, {
            name: 'Lost Packets',
            data: recLostData
        }]
    });
});