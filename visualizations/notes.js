function grandStaff() {
  var notes = [];
  var maxWidth = 600;
  var height = 300;

  function staff(selection) {
    selection.each(function(data) {
      var noteBox = 27;
      var rScale = 9;
      var rBackground = 6;
      // get the lowest and highest note represented in the data
      var maxValue = Math.max(40, d3.max(data, function(d) { return d.ix; }));
      var minValue = Math.min(16, d3.min(data, function(d) { return d.ix; }));
      var maxWidth = d3.max(data, function(d) { return d.t + d.l; });
      // compute the note radius scaled by the SVG height
      var height = (maxValue - minValue + 2) * 14;
      // function to get the Y-value given a note index
      var getY = function(ix) { return (maxValue - ix) * rScale; };
      // compute the width of the SVG
      width = (maxWidth + 2) * noteBox;
      // set up our SVG
      var svg = d3.select(this).append('svg')
          .attr('height', height)
          .attr('width', width);
      // render the grand staff
      var staffIndices = [18, 20, 22, 24, 26, 30, 32, 34, 36, 38];
      var staffLines = svg
          .selectAll('line')
          .data(staffIndices).enter()
        .append('line')
          .attr('x1', 0).attr('x2', width)
          .attr('y1', getY).attr('y2', getY);
      // render the note lines
      var noteLines = svg
          .selectAll('.notelines')
          .data(data.filter(function(d) { return d.ix % 2 === 0; })).enter()
        .append('line')
          .attr('x1', function(d) { return (d.t + 1) * noteBox; })
          .attr('x2', function(d) { return (d.t + d.l + 1) * noteBox; })
          .attr('y1', function(d) { return getY(d.ix); })
          .attr('y2', function(d) { return getY(d.ix); });
      // render the notes -- this desperately needs refactoring
      var getWidth = function(d, r) { return (d.l - 1) * noteBox + r * 2; }
      var notes = svg
          .selectAll('rect')
          .data(data).enter()
        .append('rect')
          .attr('x', function(d) { r = d.c == 'b' ? rBackground : rScale; return (d.t + 1) * noteBox + (noteBox * d.l - getWidth(d, r)) / 2; })
          .attr('y', function(d) { r = d.c == 'b' ? rBackground : rScale; return getY(d.ix) - r; })
          .attr('width', function(d) { return d.c == 'b' ? getWidth(d, rBackground) : getWidth(d, rScale); })
          .attr('height', function(d) { return d.c == 'b' ? rBackground*2 : rScale*2; })
          .attr('rx', rScale).attr('ry', rScale)
          .attr('class', function(d) { return d.c; });
      // render the accidentals
      var accidentals = svg
          .selectAll('text')
          .data(data).enter()
        .append('text')
          .attr('x', function(d) { r = d.c == 'b' ? rBackground : rScale; return (d.t + d.l + 1) * noteBox - noteBox / r; })
          .attr('y', function(d) { return getY(d.ix); })
          .text(function(d) { return d.acc; })
          .attr("fill", function(d) { if (d.c === 'b') { return "#AA830E"; } else if (d.c === 'c') { return "#307B83"; } else { return "#BD4932"; }});
    });
  }

  staff.notes = function(value) {
    if (!arguments.length) return notes;
    notes = value;
    if (typeof updateNotes === 'function') updateNotes();
    return staff;
  }

  staff.destroy = function() {
    staff.svg.remove();
    return delete staff.svg;
  }

  return staff;
}

d3.json("./output.json", function(root) {
  var notes = grandStaff();
  d3.select('#notes')
    .datum(root.s)
    .call(notes);
});
