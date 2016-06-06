// solution, index are already global from template

$("nav button").on('click', function() {
  var delta = (this.id == 'prev') ? -1 : 1,
    nextIndex = (index + delta + solutions.length) % solutions.length;
  goToNewSolution(nextIndex);
});

function goToNewSolution(n) {
  index = n;
  solution = solutions[index];
  $("#index").text(index + 1);
  drawSolution(solution);
}

function drawSolution(soln) {
  "use strict";
  var size = soln.length,
    val, x, y;
  for (x = 0; x < size; x++) {
    for (y = 0; y < size; y++) {
      val = soln[y][x];
      updateSquare(x, y, val);
    }
  }
}

function updateSquare(x, y, isFull) {
  "use strict";
  var content = isFull ? '♕' : ' ';
  getSquare(x, y).text(content);
}

function getSquare(x, y) {
  "use strict";
  return $("#" + x + "-" + y);
}
