// Set the dimensions and margins of the graph
const mt = 20, mr = 20, mb = 30, ml = 50;
const fWidth = 600, fHeight = 350;
const width = fWidth - ml - mr, height = fHeight - mt - mb;


// Set the ranges
let x = d3.scaleTime().range([0, width]);
let y = d3.scaleLinear().range([height, 0]);

// Define the area
let area = d3.area()
    .x(d => x(d.date))
    .y0(height)
    .y1((d) => y(d.litterCount));

// Define the line
let litterLine = d3.line()
    .x((d) => x(d.date))
    .y((d) => y(d.litterCount));

// Create the SVG
let svg = d3.select("#graph").append("svg")
    // .attr('width', fWidth)
    // .attr('height', fHeight)
    .attr("viewBox", `0 0 ${fWidth} ${fHeight}`)
    .append("g")
    // Move the group element to the top left margin
    .attr("transform", `translate(${ml}, ${mt})`);

// Scale the range of the data
x.domain(d3.extent(data, d => d.date));
y.domain([0, d3.max(data, d => d.litterCount)]);

// Add the area
svg.append("path")
    .data([data])
    .attr("class", "area")
    .attr("d", area);

// Add the line path.
svg.append("path")
    .data([data])
    .attr("class", "line")
    .attr("d", litterLine);

// Add the X Axis
svg.append("g")
    .attr("transform", `translate(0, ${height})`)
    .attr("class", "axes")
    .call(d3.axisBottom(x));

// Add the Y Axis
svg.append("g")
    .attr("class", "axes")
    .call(d3.axisLeft(y));

// Add the header
svg.append('text')
    .attr('x', width / 2)
    .attr('y', 0)
    .attr('class', 'header')
    .text('Litter count');
