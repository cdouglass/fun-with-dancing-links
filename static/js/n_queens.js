// solution, index are already global from template
var index = 0;

$(window).bind('popstate', function(event) {
  var url = location.href,
    queryString = '?' + url.split('?')[1];
  $.ajax('/n_queens_board_only' + queryString).done(function(response) {
    $('#board-container').html(response);
    $('#solutions-info').css('opacity', 0);
    $.ajax('/n_queens_solutions_only' + queryString).done(function(response) {
      pollBackgroundTask(response['Location'], response['task_id']);
    });
  });
});

$(document).on('ajaxStart', function() {
  $('#spinner').animate({opacity: 1}, 400).animate({opacity: 0}, 400);
});

$(document).ready(function() {
  $('nav button').prop('disabled', false);
});

$('nav button').on('click', function() {
  var delta = (this.id == 'prev') ? -1 : 1,
    nextIndex = index + delta + solutions.length;
  goToNewSolution(nextIndex);
});

$('form').on('submit', function(event) {
  var boardSize = $('input[name="n"]').val(),
    queryString = '?n=' + boardSize;
  console.log("submitted form with contents " + boardSize);
  solutions = [];
  event.preventDefault();
  history.pushState({}, '', '/n_queens' + queryString);
  $.ajax('/n_queens_board_only' + queryString).done(function(response) {
    $('#board-container').html(response);
    console.log("done");
    $('#solutions-info').css('opacity', 0);
    $.ajax('/n_queens_solutions_only' + queryString).done(function(response) {
      pollBackgroundTask(response['Location'], response['task_id']);
    });
  });
});

function pollBackgroundTask(responseUrl, taskId) {
  $.getJSON(responseUrl, {task_id: taskId}, function(data) {
    if ('result' in data && data['result']['status'] != 'PENDING') {
      solutions = data['result']; // global
      $('#solution_count').text(solutions.length);
      $('#solutions-info').delay(600).animate({opacity: 1}); // arg to show makes it into an animation, which lets delay affect it, which prevents this from showing before spinner has faded
      $('nav button').prop('disabled', false);
      $('#spinner').finish();
      if(solutions.length > 0) {
        goToNewSolution(0)
      }
    } else {
      setTimeout(function() {
        pollBackgroundTask(responseUrl, taskId);
      }, 10);
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
