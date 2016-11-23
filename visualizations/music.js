var vis = d3.select('#notes')
    .append('svg');
var w = 900,
    h = 400;

vis.attr('width', w)
    .attr('height', h);

var staff = [0, 1, 2, 3, 4];
var staff = staff.map(function(d) { return { 'y': (d+1)*20 }; })

vis.selectAll('.staff')
    .data(staff)
    .enter()
    .append('line')
    .attr('x1', function(d) { return  10; })
    .attr('x2', function(d) { return 410; })
    .attr('y1', function(d) { return d.y; })
    .attr('y2', function(d) { return d.y; })
    .style('stroke', 'rgb(10, 10, 10)');

var notes = [{ 'n1': -1, 'n2': 5 },
	     { 'n1': -1, 'n2': 4 },
	     { 'n1': 3, 'n2': 3 },
	     { 'n1': 2, 'n2': 2 },
	     { 'n1': 1, 'n2': -1 }];

vis.selectAll('.notes')
    .data(notes)
    .enter()
    .append('circle')
    .attr('cx', function(d, i) { return i*30+30; })
    .attr('cy', function(d) { if(d.n2 >= 0) { return 100 - d.n2 * 10; } else { return -1000; } })
    .attr('r', '10px')
    .attr('fill', 'rgba(10, 10, 10)');
