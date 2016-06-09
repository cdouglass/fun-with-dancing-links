// solution, index are already global from template
var index = $('#index').text();

$('nav button').on('click', function() {
  var delta = (this.id == 'prev') ? -1 : 1,
    nextIndex = (index + delta + solutions.length) % solutions.length;
  goToNewSolution(nextIndex);
});

$('form').on('submit', function(event) {
  console.log("hi!!!");
  event.preventDefault();
  $.ajax('/n_queens', {
    method: 'POST',
    data: 'board_size=' + $('input[name="board_size"]').val()
  }).done(function(response) {
    document.open();
    document.write(response);
    document.close();
  }); // TODO get a smaller response and don't reload everything
});

function goToNewSolution(n) {
  if (solutions.length > 0) {
    index = n;
    solution = solutions[index];
    $('#index').text(index + 1);
    drawSolution(solution);
  }
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
  return $('#' + x + '-' + y);
}
