// solution, index are already global from template
var index = 0;

$('nav button').on('click', function() {
  var delta = (this.id == 'prev') ? -1 : 1,
    nextIndex = index + delta + solutions.length;
  goToNewSolution(nextIndex);
});

$('form').on('submit', function(event) {
  var board_size = $('input[name="board_size"]').val();
  event.preventDefault();
  $.ajax('/n_queens', {method: 'POST', data: 'board_size=' + board_size}).done(function(response) {
    // not replacing whole container as that would break nav buttons
    var board = $($.parseHTML(response)).find('#board');
    $('#board').replaceWith(board);
    var solutions_info = $($.parseHTML(response)).find('#solutions-info');
    $('#solutions-info').replaceWith(solutions_info);
    $.ajax('/n_queens_solutions_only', {
      method: 'POST',
      data: 'board_size=' + board_size
    }).done(function(response) {
      pollBackgroundTask(response['Location'], response['task_id']);
    });
  });
});

function pollBackgroundTask(response_url, task_id) {
  $.getJSON(response_url, {task_id: task_id}, function(data) {
    if ('result' in data && data['result']['status'] != 'PENDING') {
      solutions = data['result']; // global
      $('#solution_count').text(solutions.length);
      if(solutions.length > 0) {
        goToNewSolution(0)
      }
    } else {
      setTimeout(function() {
        pollBackgroundTask(response_url, task_id);
      }, 2000);
    }
  });
}

function goToNewSolution(n) {
  if (solutions.length > 0) {
    index = n % solutions.length;
    console.log('going to new solution with index ' + index)
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
