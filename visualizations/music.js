var svg = d3.select('#notes').append('svg');

d3.json("./output.json", function(root) {
  update(root.s1, root.s2);
});

var update = function(s1, s2) {
  svg.attr('width', 500).attr('height', 560);
  var stuff = staff();

  /*
  var staff = [0, 1, 2, 3, 4, 6, 7, 8, 9, 10].map(
    function(d) {
      return { 'y': 200 + (d+1)*18 };
    }
  );

  var getXPos = function(d, i) { return i * 22 + 30; };

  var getYPos = function(d) {
    if (d.ix !== null) { return 560 - d.ix * 9; } else { return 10000; }
  };

  var getIncorrect = function(d, i) {
    return s1[i].ix !== s2[i].ix || s1[i].acc !== s2[i].acc;
  };

  var getCorrect = function(d, i) {
    return s1[i].ix === s2[i].ix && s1[i].acc === s2[i].acc;
  };

  var getAccidentals = function(d) {
    return d.acc !== null;
  }

  var w = 40 + (s1.length + 1) * 22,
      h = 560;

  svg.attr('width', w).attr('height', h);

  var staff = svg.selectAll('.staff')
      .data(staff)
    .enter().append('line')
      .attr('x1', function(d) { return 10; })
      .attr('x2', function(d) { return w - 20; })
      .attr('y1', function(d) { return d.y; })
      .attr('y2', function(d) { return d.y; });

  var s2Data = svg.selectAll('.s2')
      .data(s2).enter();

  var s2Lines = s2Data
      .append('line').attr('x1', function(d, i) { return getXPos(d, i) - 14; })
      .attr('x2', function(d, i) { return getXPos(d, i) + 14; })
      .attr('y1', function(d) { if(d.ix % 2 == 0) { return getYPos(d); } else { return 10000; } })
      .attr('y2', function(d) { if(d.ix % 2 == 0) { return getYPos(d); } else { return 10000; } });

  var s2Notes = s2Data
      .append('circle')
      .attr('cx', getXPos);

  var s2Incorrect = s2Notes
    .filter(getIncorrect)
      .attr('cy', getYPos)
      .attr('class', 'incorrect-background');

  var s2Acc = s2Data
      .append('text')
      .attr('x', function(d, i) { return getXPos(d, i) + 5; })
    .filter(function(d, i) { return getAccidentals(d) && getIncorrect(d, i); })
      .attr('y', getYPos)
      .text(function(d, i) { return "#"; })
      .attr("fill", "#AA830E");

  var s1Data = svg.selectAll('.s1')
      .data(s1).enter();

  var s1Lines = s1Data
      .append('line').attr('x1', function(d, i) { return getXPos(d, i) - 14; })
      .attr('x2', function(d, i) { return getXPos(d, i) + 14; })
      .attr('y1', function(d) { if(d.ix % 2 == 0) { return getYPos(d); } else { return 10000; } })
      .attr('y2', function(d) { if(d.ix % 2 == 0) { return getYPos(d); } else { return 10000; } });

  var s1Notes = s1Data
      .append('circle')
      .attr('cx', getXPos);

  var s1Incorrect = s1Notes
    .filter(getIncorrect)
      .attr('cy', getYPos)
      .attr('class', 'incorrect');

  // There has to be a DRY-er way to do this whole thing
  var s1Acc = s1Data
      .append('text')
      .attr('x', function(d, i) { return getXPos(d, i) + 5; })
    .filter(function(d, i) { return getAccidentals(d) && getIncorrect(d, i); })
      .attr('y', getYPos)
      .text(function(d, i) { return "#"; })
      .attr("fill", "#BD4932");

  var correct = s1Notes
    .filter(getCorrect)
      .attr('cy', getYPos)
      .attr('class', 'correct');

  var correctAcc = s1Data
      .append('text')
      .attr('x', function(d, i) { return getXPos(d, i) + 5; })
    .filter(function(d, i) { return getAccidentals(d) && getCorrect(d, i); })
      .attr('y', getYPos)
      .text(function(d, i) { return "#"; })
      .attr("fill", "#307B83");*/

}
