var notes = 'CDEFGAB';

var noteToIndex = function(note) {
  if(note === '-') { return null; }

  i = notes.indexOf(note[0]);
  o = parseInt(note.slice(-1));

  return o*7+i;
}

var accidentals = function(note) {
  if(note.length < 3) { return null; }
  return note[1];
}

var zip_to_dict = function(sequence) {
  ns = [];
  for(i = 0; i < sequence.length; i++) {
    ns.push({
      'ix': noteToIndex(sequence[i]),
      'acc': accidentals(sequence[i])
    });
  }
  return ns;
}

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

var s1 = zip_to_dict(['C4', 'D4', 'E4', 'F4', '-']);
var s2 = zip_to_dict(['-', '-', 'E4', 'F4', 'G4']);

vis.selectAll('.notes')
    .data(s1)
    .enter()
    .append('circle')
    .attr('cx', function(d, i) { return i*30+30; })
    .attr('cy', function(d) { if(d.ix !== null) { return 100 - d.ix; } else { return -1000; } })
    .attr('r', '10px')
    .attr('fill', 'rgba(10, 10, 10)');
