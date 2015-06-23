$(function () {
    for(var graph in activeGraphs){
        $('#'+graph).highcharts(activeGraphs[graph]);
    }
});