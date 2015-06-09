import json
jsonTemplate = "{chart:{type:'%(type)s'},title:{text:'%(title)s'},xAxis:{type:'linear',title:{text:'%(xtitle)s'}},yAxis:{title:{text:'%(xtitle)s'},min:%(ymin)d},plotOptions:{spline:{marker:{enabled:'%(marker)s'}}},series:%(seriesjson)s}"

class Graph:
    def __init__(self, type="line", title="Title", xtitle="X-Axis", ytitle="Y-Axis", ymin=0, marker="true"):
        self.type=type
        self.title=title
        self.xtitle=xtitle
        self.ytitle=ytitle
        self.ymin=ymin
        self.marker=marker
        self.series=[]

    def addSeries(self, title, data):
        self.series.append(dict(name=title, data=data))

    def toJson(self):
        formatDict = dict(type=self.type,
                          title=self.type,
                          xtitle=self.xtitle,
                          ytitle=self.ytitle,
                          ymin=self.ymin,
                          marker=self.marker,
                          seriesjson=json.dumps(self.series))
        return jsonTemplate % formatDict
