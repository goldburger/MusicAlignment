var svg = d3.select('#notes').append('svg');

d3.json("./output.json", function(root) {
  update(root.s1, root.s2);
});

var update = function(s1, s2) {
  var staff = [0, 1, 2, 3, 4, 6, 7, 8, 9, 10].map(
    function(d) {
      return { 'y': 200 + (d+1)*14 };
    }
  );

  var w = 40 + (s1.length + 1) * 18,
      h = 560;

  svg.attr('width', w).attr('height', h);

  var staff = svg.selectAll('.staff')
      .data(staff)
    .enter().append('line')
      .attr('x1', function(d) { return 10; })
      .attr('x2', function(d) { return w - 20; })
      .attr('y1', function(d) { return d.y; })
      .attr('y2', function(d) { return d.y; })
      .style('stroke', '#444444');

  var secondSequenceIncorrect = svg.selectAll('.s2')
      .data(s2)
    .enter().append('circle')
      .attr('cx', function(d, i) { return i * 18 + 30; })
    .filter(function(d, i) { return (d.ix !== s1[i].ix) || (d.acc !== s1[i].acc) })
      .attr('cy', function(d) { if (d.ix !== null) { return 480-d.ix * 7; } else { return 10000;  } })
      .attr('class', 'incorrect-background');

  var firstSequence = svg.selectAll('.s1')
      .data(s1)
    .enter().append('circle')
      .attr('cx', function(d, i) { return i * 18 + 30; });

  var correct = firstSequence
    .filter(function(d, i) { return (d.ix === s2[i].ix) && (d.acc === s2[i].acc) })
      .attr('cy', function(d) { return 480-d.ix * 7; })
      .attr('class', 'correct');

  var firstSequenceIncorrect = firstSequence
    .filter(function(d, i) { return (d.ix !== s2[i].ix) || (d.acc !== s2[i].acc) })
      .attr('cy', function(d) { if (d.ix !== null) { return 480-d.ix * 7; } else { return 10000;  } })
      .attr('class', 'incorrect');
}
