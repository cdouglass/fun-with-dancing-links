// solution, index are already global from template
var index = 0;

$('nav button').on('click', function() {
  var delta = (this.id == 'prev') ? -1 : 1,
    nextIndex = index + delta + solutions.length;
  goToNewSolution(nextIndex);
});

$('form').on('submit', function(event) {
  var boardSize = $('input[name="board_size"]').val(),
    queryString = '?n=' + boardSize;
  //location.assign('/n_queens' + queryString); // TODO can I assign location without actually sending a GET request and thereby defeatin ght entire purpose of this ajax shit?
  event.preventDefault();
  $.ajax('/n_queens_board_only' + queryString).done(function(response) {
    // not replacing whole container as that would break nav buttons
    $('#board').replaceWith($($.parseHTML(response)).find('#board'));
    $('#solutions-info').replaceWith($($.parseHTML(response)).find('#solutions-info'));
    $.ajax('/n_queens_solutions_only' + queryString).done(function(response) {
      console.log('hi');
      pollBackgroundTask(response['Location'], response['task_id'], 100);
    });
  });
});

function pollBackgroundTask(responseUrl, taskId, timeOut) {
  console.log('polling at ' + Date.now());
  $.getJSON(responseUrl, {task_id: taskId}, function(data) {
    if ('result' in data && data['result']['status'] != 'PENDING') {
      console.log('REQUEST COMPLETED');
      solutions = data['result']; // global
      $('#solution_count').text(solutions.length);
      if(solutions.length > 0) {
        goToNewSolution(0)
      }
    } else {
      setTimeout(function() {
        pollBackgroundTask(responseUrl, taskId);
      }, timeOut * 1.5);
    }
  });
}

function goToNewSolution(n) {
  if (solutions.length > 0) {
    index = n % solutions.length;
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
