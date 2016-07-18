/*jslint browser:true, indent:2*/
/*global $, solutions:true*/
var index = 0,
  solution = solutions[index];

function getSquare(x, y) {
  "use strict";
  return $('#' + x + '-' + y);
}

function updateSquare(x, y, isFull) {
  "use strict";
  var content = isFull ? '♕' : ' ';
  getSquare(x, y).text(content);
}

function drawSolution(soln) {
  "use strict";
  var size = soln.length,
    val,
    x,
    y;
  for (x = 0; x < size; x += 1) {
    for (y = 0; y < size; y += 1) {
      val = soln[y][x];
      updateSquare(x, y, val);
    }
  }
}

function goToNewSolution(n) {
  "use strict";
  if (solutions.length > 0) {
    index = n % solutions.length;
    solution = solutions[index];
    $('#index').text(index + 1);
    drawSolution(solution);
  }
}

function pollBackgroundTask(responseUrl, taskId) {
  "use strict";
  $.getJSON(responseUrl, {task_id: taskId}, function (data) {
    if (data.hasOwnProperty('result') && data.result.status !== 'PENDING') {
      solutions = data.result; // global
      $('#solution_count').text(solutions.length);
      $('#solutions-info').delay(600).animate({opacity: 1});
      $('button').prop('disabled', false);
      $('#spinner').removeClass('loading');
      if (solutions.length > 0) {
        goToNewSolution(0);
      }
    } else {
      setTimeout(function () {
        pollBackgroundTask(responseUrl, taskId);
      }, 500);
    }
  });
}

$(window).bind('popstate', function () {
  "use strict";
  var url = location.href,
    queryString = '?' + url.split('?')[1];
  $.ajax('/n_queens_board_only' + queryString).done(function (response) {
    $('#solutions-info').css('opacity', 0);
    $('#board-container').html(response);
    $.ajax('/n_queens_solutions_only' + queryString).done(function (response) {
      pollBackgroundTask(response.Location, response.task_id);
    });
  });
});

$(document).ready(function () {
  "use strict";
  $('button').prop('disabled', false);
});

$('button').on('click', function () {
  "use strict";
  var delta = (this.id === 'prev') ? -1 : 1,
    nextIndex = index + delta + solutions.length;
  goToNewSolution(nextIndex);
});

$('form').on('submit', function (event) {
  "use strict";
  var boardSize = $('input[name="n"]').val(),
    queryString = '?n=' + boardSize;
  solutions = [];
  event.preventDefault();
  history.pushState({}, '', '/n_queens' + queryString);
  $.ajax('/n_queens_board_only' + queryString).done(function (response) {
    $('#board-container').html(response);
    solutions = [];
    $('#spinner').addClass('loading');
    $('#solutions-info').css('opacity', 0);
    $.ajax('/n_queens_solutions_only' + queryString).done(function (response) {
      pollBackgroundTask(response.Location, response.task_id);
    });
  });
});
