require.config({
  paths: {
    d3: "https://d3js.org/d3.v7.min",
  },
});

// Everything is wrapped in this require.js function - this way the variables don't
// go into the global scope and everything works even when multiple graphs are
// rendered.
require(["d3"], function (d3) {
  const CHART_SELECTOR = dummyData ? "#chart" : "#chart-${chart_id}";
  const TOOLTIP_SELECTOR = dummyData ? "#tooltip" : "#tooltip-${chart_id}";
  const svg_chart = document.getElementById("svg-chart");
  const tooltip = document.getElementById("tooltip");

  // Maintain the svg element the tooltip is currently bound to.
  let tooltipNode = null;
  const tooltipTable = tooltip.querySelector(".tooltip-table");

  // Maintain the currently selected node, if any, as well as all nodes/links
  // related to it.
  // When not null, it will have the following:
  // {
  //  baseNodeId: (the index of the base node being selected),
  //  connectedNodeIds: (an array of all connected node ids),
  //  connectedLinkIds: (an array of all connected link ids),
  // };
  let selectedNode = null;

  // Dynamically set the id of the svg and tooltip.
  // If in development mode (i.e. dummyData is not null), the id will just be
  // "#chart" or "#tooltip" respectively.
  svg_chart.id = CHART_SELECTOR.substring(1, CHART_SELECTOR.length);
  tooltip.id = TOOLTIP_SELECTOR.substring(1, TOOLTIP_SELECTOR.length);
  let data = {};
  if (dummyData) {
    data = dummyData;
  } else {
    data = {
      nodes: JSON.parse("${nodes}".replace(/'/g, '"')),
      links: JSON.parse("${links}".replace(/'/g, '"')),
    };
  }

  /* Code found in a range of places, spliced together from the following:
    https://observablehq.com/@brunolaranjeira/d3-v6-force-directed-graph-with-directional-straight-arrow
    https://bl.ocks.org/mbostock/4062045
    https://github.com/nlp-tlp/aquila/blob/master/views/visualisations/entity_linking_graph.jade
    https://observablehq.com/@harrylove/draw-an-arrowhead-marker-connected-to-a-line-in-d3
    */

  // https://stackoverflow.com/questions/5560248/programmatically-lighten-or-darken-a-hex-color-or-rgb-and-blend-colors
  function lightenDarkenColor(col, amt) {
    let usePound = false;
    if (col[0] == "#") {
      col = col.slice(1);
      usePound = true;
    }

    let num = parseInt(col, 16);

    let r = (num >> 16) + amt;

    if (r > 255) r = 255;
    else if (r < 0) r = 0;

    let b = ((num >> 8) & 0x00ff) + amt;

    if (b > 255) b = 255;
    else if (b < 0) b = 0;

    let g = (num & 0x0000ff) + amt;

    if (g > 255) g = 255;
    else if (g < 0) g = 0;

    return (usePound ? "#" : "") + (g | (b << 8) | (r << 16)).toString(16);
  }

  /**
   * Set the tooltip (after hovering over a specific node). The tooltip, which appears
   * on the right of the graph, will show the property (key, value) pairs of the
   * selected node.
   * @param {[type]} d The d3 data point.
   * @param {[type]} i The object.
   */
  function setTooltip(d, i) {
    var p = Object.getPrototypeOf(i);
    const keys = Object.keys(p);
    const vals = keys.map((key) => p[key]);

    let table = "";
    for (var j = 0; j < keys.length; j++) {
      table += "<tr>";
      table += `<td>${keys[j]}:</td>`;
      table += `<td>${vals[j]}</td>`;
      table += "</tr>";
    }

    tooltipTable.innerHTML = table;
    tooltip.style.opacity = "0.95";

    tooltipNode = d.target;
    updateTooltipPosition();

    return d;
  }

  /**
   * Update the position (x and y coords) of the tooltip based on the location
   * of the element it is bound to.
   * @return {[type]} [description]
   */
  function updateTooltipPosition() {
    if (!tooltipNode) return;
    const rect = tooltipNode.getBoundingClientRect();
    const tooltipRect = tooltip.getBoundingClientRect();
    const svgRect = svg_chart.getBoundingClientRect();

    tooltip.style.left = `${rect.right + 25 - svgRect.left}px`;
    tooltip.style.top = `${
      (rect.top + rect.bottom) / 2 - tooltipRect.height / 2 - svgRect.top
    }px`;
  }

  /**
   * Clear the tooltip by settings its opacity to 0.
   * @return {[type]} [description]
   */
  function clearTooltip() {
    tooltip.style.opacity = "0";
  }

  /**
   * Allow the nodes to be moved around when dragged.
   * @param  {[type]} simulation [description]
   * @return {[type]}            [description]
   */
  let drag = (simulation) => {
    function dragstarted(event) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      event.subject.fx = event.subject.x;
      event.subject.fy = event.subject.y;
    }

    function dragged(event) {
      event.subject.fx = event.x;
      event.subject.fy = event.y;
    }

    function dragended(event) {
      if (!event.active) simulation.alphaTarget(0);
      event.subject.fx = null;
      event.subject.fy = null;
    }

    return d3
      .drag()
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended);
  };

  const scale = d3.scaleOrdinal(d3.schemeCategory10);

  const nodeSize = 40;
  let height = 600;
  let width = 600;

  const links = data.links.map((d) => Object.create(d));
  const nodes = data.nodes.map((d) => Object.create(d));

  // A list of colours that the colour map will be generated from.
  const colours = [
    "#99ffcc",
    "#ffcccc",
    "#ccccff",
    "#ccff99",
    "#ccffcc",
    "#ccffff",
    "#ffcc99",
    "#ffccff",
    "#ffff99",
    "#ffffcc",
    "#cccc99",
    "#fbafff",
  ];

  /**
   * Load the 'colour map' (i.e. mapping of category to colour).
   * @param  {Array} nodes The node data.
   * @return {Object}       The colour map.
   */
  function loadColourMap(nodes) {
    let colourMap = {};
    // Load the colour map
    for (let i = 0; i < nodes.length; i++) {
      const category = nodes[i].category;
      if (!(category in colourMap)) {
        colourMap[category] =
          colours[Object.keys(colourMap).length % colours.length];
      }
    }
    return colourMap;
  }
  colourMap = loadColourMap(nodes);
  const getColour = (d) => {
    return colourMap[d.category];
  };

  // Initialise some d3 forces etc to make the graph behave properly.
  const simulation = d3
    .forceSimulation(nodes)
    .force(
      "link",
      d3.forceLink(links).id((d) => d.id)
    )
    .force("charge", d3.forceManyBody().strength(-300))
    .force(
      "collide",
      d3.forceCollide((d) => nodeSize * 1.5)
    )
    .force("center", d3.forceCenter(width / 2, height / 2));

  // Svg: the main container for rendering the graph.
  const svg = d3.select(CHART_SELECTOR).attr("viewBox", [0, 0, width, height]);

  // svg_g: The 'g' within svg, which seems to make zooming/panning smoother
  const svg_g = svg.append("g");
  const defs = svg_g.append("defs");

  // Marker: a definition for the triangles appearing at the end of each link.
  const marker = defs
    .selectAll("marker")
    .data(["type_1"])
    .enter()
    .append("svg:marker")
    .attr("id", function (d, i) {
      return `marker_${i}`;
    })
    .attr("viewBox", "0 -5 10 10")
    .attr("refX", nodeSize + 3)
    .attr("refY", 0)
    .attr("markerWidth", 6)
    .attr("markerHeight", 6)
    .attr("orient", "auto")
    .append("svg:path")
    .attr("fill", "#444")
    .attr("d", "M0,-5L10,0L0,5");

  // Link: The links between nodes.
  const link = svg_g
    .append("g")
    .attr("id", "links")
    .attr("fill", "none")
    .attr("stroke-width", 1.5)
    .selectAll("path")
    .data(links)
    .enter()
    .append("path")
    .attr("stroke", "#444")
    .attr("stroke-width", 2)
    .attr("marker-end", function (d, i) {
      return `url("#marker_0")`;
    })
    .attr(
      "d",
      (d) =>
        `M${d.source.x},${d.source.y}A0,0 0 0,1 ${d.target.x},${d.target.y}`
    );

  /**
   * When the mouse is unclicked, clear the selectedNode.
   * This will remove the 'hide' class from all nodes in the tick function.
   */
  function deselectNode() {
    selectedNode = null;
  }

  /**
   * When a node is clicked, update selectedNode to reflect the id of that node,
   * as well as the id of all nodes and links connected to it.
   * @param  {[type]} d [description]
   * @param  {[type]} i [description]
   * @return {Object}   The selectedNode
   *                    (baseNodeId, connectedNodeIds, connectedLinkIds).
   */
  function selectNode(d, i) {
    let connectedNodeIds = new Set();
    let connectedLinkIds = new Set();
    for (let link of links) {
      console.log(link.source.index, i);
      if (link.source.index === i.index || link.target.index === i.index) {
        connectedLinkIds.add(link.index);
        if (link.source.index === i.index) {
          connectedNodeIds.add(link.target.index);
        } else if (link.target === i.index) {
          connectedNodeIds.add(link.source.index);
        }
      }
    }
    selectedNode = {
      baseNodeId: i.index,
      connectedNodeIds: connectedNodeIds,
      connectedLinkIds: connectedLinkIds,
    };
  }

  // Node: The nodes.
  const node = svg_g
    .append("g")
    .attr("stroke-width", 3)
    .selectAll("circle")
    .data(nodes)
    .join("circle")
    .attr("class", "node")
    .attr("r", nodeSize)
    .attr("fill", getColour)
    .attr("stroke", function (d) {
      return lightenDarkenColor(getColour(d), -15);
    })
    .on("mousedown", selectNode)
    .call(drag(simulation));

  // When a node is hovered over, set the tooltip accordingly.
  // Clear the tooltip when the mouse leaves a node.
  d3.selectAll(".node").on("mouseover", setTooltip);
  d3.selectAll(".node").on("mouseleave", clearTooltip);

  // When mouse up event (or pointer up event) fires, deselect the
  // selected node if there is one.
  document.addEventListener("mouseup", deselectNode);
  document.addEventListener("pointerup", deselectNode);

  // Text: The text appearing on the nodes.
  const text = svg_g
    .append("g")
    .selectAll("text")
    .data(nodes)
    .enter()
    .append("text")
    .text((d) => d.name)
    .attr("font-size", 12)
    .attr("text-anchor", "middle")
    .attr("dominant-baseline", "central");

  // Links text: The text appearing on the links.
  const link_text = svg_g
    .append("g")
    .selectAll("text")
    .data(links)
    .enter()
    .append("text")
    .text((d) => d.type)
    .attr("font-size", 10)
    .attr("text-anchor", "middle")
    .attr("dominant-baseline", "central");

  // Every time the simulation ticks, update the path of the links,
  // the location of the nodes, the location of the text, and also the
  // tooltip position.
  simulation.on("tick", () => {
    link.attr(
      "d",
      (d) =>
        `M${d.source.x},${d.source.y}A0,0 0 0,1 ${d.target.x},${d.target.y}`
    );

    node.attr("cx", (d) => d.x).attr("cy", (d) => d.y);
    text.attr("x", (d) => Math.floor(d.x)).attr("y", (d) => Math.floor(d.y));
    link_text
      .attr("x", (d) => (d.source.x + d.target.x) / 2)
      .attr("y", (d) => (d.source.y + d.target.y) / 2);
    updateTooltipPosition();

    // If a node is currently selected, add a class to the nodes that are not
    // related to that node.
    //

    node.classed("hide", function (d, i) {
      return (
        selectedNode &&
        selectedNode.baseNodeId !== i &&
        !selectedNode.connectedNodeIds.has(i)
      );
    });

    text.classed("hide", function (d, i) {
      return (
        selectedNode &&
        selectedNode.baseNodeId !== i &&
        !selectedNode.connectedNodeIds.has(i)
      );
    });

    link.classed("hide", function (d, i) {
      return selectedNode && !selectedNode.connectedLinkIds.has(i);
    });

    link_text.classed("hide", function (d, i) {
      return selectedNode && !selectedNode.connectedLinkIds.has(i);
    });
  });

  // Register the zoom handler.
  let zoom = d3.zoom().on("zoom", handleZoom);

  /**
   * A function to handle zooming/panning. Sets a transform on the svg_g container
   * according to the zoom/pan level.
   * @param  {[type]} e [description]
   * @return {[type]}   [description]
   */
  function handleZoom(e) {
    transform = e.transform;
    svg_g.attr("transform", e.transform);
    text.attr("font-size", 12 / e.transform.k ** 0.7);
    link_text.attr("font-size", 10 / e.transform.k ** 0.7);
  }

  // Initialise the zooming.
  function initZoom() {
    svg.call(zoom);
  }

  initZoom();

  // If dummyData is present (i.e. dev mode), display a message at the bottom.
  if (dummyData) {
    let div = document.createElement("div");
    div.innerHTML =
      "<h3>Note: currently in development mode using dummy data.</h3>";
    document.body.appendChild(div);
  }
});
