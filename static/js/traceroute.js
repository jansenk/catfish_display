
// Create a new directed graph
var g = new dagreD3.graphlib.Graph()
                   .setGraph({})
                   .setDefaultEdgeLabel(function() { return {}; });

// Add hops and edges to the graph
console.log(hops)
for(var i = 0; i < hops.length; i++){
  console.log(hops[i]);
  hops[i].rx = hops[i].ry = 5;
  g.setNode(i, hops[i]);
  console.log("Added node ", i, hops[i]);
  if(i > 0) {
    g.setEdge(i-1, i);
    console.log("Added edge from %d to %d", i-1, i);
  }
}
var index = 0;
console.log(index++);
// Create the renderer
var render = new dagreD3.render();
console.log(index++);
// Set up an SVG group so that we can translate the final graph.
var svg = d3.select("svg"),
    svgGroup = svg.append("g");
console.log(index++);
// Run the renderer. This is what draws the final graph.
render(d3.select("svg g"), g);
console.log(index++);
// Center the graph
var xCenterOffset = (svg.attr("width") - g.graph().width) / 2;
console.log(index++);
svgGroup.attr("transform", "translate(" + xCenterOffset + ", 20)");
console.log(index++);
svg.attr("height", g.graph().height + 40);
console.log(index++);