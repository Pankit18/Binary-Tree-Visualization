const width = 800;
const height = 600;

const svg = d3
  .select("#tree-container")
  .append("svg")
  .attr("width", width)
  .attr("height", height)
  .style("background", "rgba(255, 255, 255, 0.1)")
  .style("border-radius", "10px")
  .style("box-shadow", "0 4px 6px rgba(0, 0, 0, 0.2)");

const g = svg.append("g").attr("transform", "translate(50, 50)");

const treeLayout = d3.tree().size([width - 100, height - 100]);
const root = d3.hierarchy(treeData);

treeLayout(root);

const link = g
  .selectAll(".link")
  .data(root.links())
  .enter()
  .append("line")
  .attr("class", "link")
  .attr("x1", (d) => d.source.x)
  .attr("y1", (d) => d.source.y)
  .attr("x2", (d) => d.source.x)
  .attr("y2", (d) => d.source.y)
  .style("stroke", "#ccc")
  .style("stroke-width", 2)
  .transition()
  .duration(1000)
  .attr("x2", (d) => d.target.x)
  .attr("y2", (d) => d.target.y);

const node = g
  .selectAll(".node")
  .data(root.descendants())
  .enter()
  .append("g")
  .attr("class", "node")
  .attr("transform", (d) => `translate(${d.x}, ${d.y})`);

node
  .append("circle")
  .attr("r", 20)
  .style("fill", "#3498db")
  .style("stroke", "#2980b9")
  .style("stroke-width", 2);

node
  .append("text")
  .attr("dy", -30)
  .attr("text-anchor", "middle")
  .style("font-size", "16px")
  .style("fill", "#fff")
  .text((d) => d.data.name);
