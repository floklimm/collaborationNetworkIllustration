let JSONFILENAME = "collaborationNetwork.json"

var svg = d3.select("area1"),
    width = +svg.attr("width"),
    height = +svg.attr("height"),
    radius = 30;

var color = d3.scaleOrdinal(d3.schemeCategory10);

var simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(function(d) { return d.id; }))
    .force("charge", d3.forceManyBody().distanceMin(20).distanceMax(300).strength(-60))
    .force("center", d3.forceCenter(width / 2, height / 2));

// Define the div for the tooltip
    var div = d3.select("body").append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);

d3.json(JSONFILENAME, function(error, graph) {
  if (error) throw error;

  var link = svg.append("g")
    .attr("class", "links")
    .selectAll("line")
    .data(graph.links)
    .enter().append("line")
      .attr("stroke-width", 4);

  var node = svg.append("g")
    .attr("class", "nodes")
    .selectAll("circle")
    .data(graph.nodes)
    .enter().append("circle")
    .attr("r", 10)
    .attr("fill", function(d) { return color(d.group); })
    .on("mouseover", function(d) {
      // make attached edges red and thicker
      link.style('stroke-width', function(l) {
       if (d === l.source || d === l.target)
         return 4;
       else
         return 2;
       });
       link.style('stroke', function(l) {
         if (d === l.source || d === l.target)
           return "red";
         else
           return "#999";
         });
         link.style('stroke-opacity',0.6);

         //increase node size
         d3.selectAll("circle").transition()
         .duration(400)
         .attr("r", 10);
         d3.select(this).transition()
          .duration(400)
          .attr("r", 15);




            // div.transition()
            //     .duration(100)
            //     .style("opacity", .9);
            // div	.html(d.name)
            //     .style("left", (d3.event.pageX) + "px")
            //     .style("top", (d3.event.pageY - 28) + "px");

                // removing text label and the image from earlier
                svg.select("#nameText").remove();
                svg.selectAll("#authorPhoto").remove();

                var text_name = svg.append("text")
                    .attr("id","nameText")
                    .attr("x", width)
                    .attr("y", height-30)
                    .attr("dy", ".35em")
                    .attr("text-anchor", "end")
                    .style("font", "100 20px Helvetica Neue")
                    .text(d.name);

                    var imgs = svg
                        .append("svg:image")
                        // .attr("xlink:href", "file:///D:/d3js_projects/refresh.png")
                        .attr("xlink:href", function(l) {
                          return d.image;
                          })
                        .attr("x", width-200)
                        .attr("y", height-250)
                        .attr("width", "200")
                        .attr("height", "200")
                        .attr("preserveAspectRatio","xMaxYMax meet")
                        .attr("id","authorPhoto")

            })
    .on("mouseout", function(d) {
                    div.transition()
                        .duration(1000)
                        .style("opacity", .0);

                    })
    .call(d3.drag()
    .on("start", dragstarted)
    .on("drag", dragged)
    .on("end", dragended))
    .on("dblclick", dblclick)
    ;


  simulation
      .nodes(graph.nodes)
      .on("tick", ticked);

  simulation.force("link")
      .links(graph.links);

      // adding github logo with link
            var imgs = svg
                .append("svg:image")
                .attr("xlink:href", "./images/GitHub-Mark-120px-plus.png")
                .attr("x", 0)
                .attr("y", height-40)
                .attr("width", "40")
                .attr("height", "40")
                .on("click", githubclick)


// // adding github logo with link
//       var imgs = svg.selectAll("image").data([0]);
//            imgs.enter()
//           .append("svg:image")
//           .attr("xlink:href", "./images/GitHub-Mark-120px-plus.png")
//           .attr("x", 0)
//           .attr("y", height-40)
//           .attr("width", "40")
//           .attr("height", "40")
//           .on("click", githubclick)


  function ticked() {


    link
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node
        .attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });

    node.attr("cx", function(d) { return d.x = Math.max(radius, Math.min(width - radius, d.x)); })
        .attr("cy", function(d) { return d.y = Math.max(radius, Math.min(height - radius, d.y)); });

  }
});

function dragstarted(d) {
  if (!d3.event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x;
  d.fy = d.y;
}

function dragged(d) {
  d.fx = d3.event.x;
  d.fy = d3.event.y;
}

function dragended(d) {
  if (!d3.event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
}


 function dblclick(a){
   window.location.assign(a.url, '_blank');
}

 function githubclick(a){
     window.location.assign("https://github.com/floklimm/collaborationNetworkIllustration", '_blank');
  }
