/*jslint browser: true, indent:2*/
/*global $, clueSet, solution*/
var board = $("#board"),
  digits = [1, 2, 3, 4, 5, 6, 7, 8, 9],
  partialSolution,
  r;

function chooseRandomFromArr(arr) {
  "use strict";
  var len = arr.length,
    index = Math.floor(Math.random() * len);
  return arr[index];
}

function tempHighlight(elt, options) {
  "use strict";
  if (options === undefined) {
    options = {color: 'yellow', duration: '3s', next: 'inherit'};
  }
  elt.css('background-color', options.color);
  setTimeout(function () {
    elt.css({'background-color': options.next, 'transition-duration': options.duration, 'transition-property': 'background-color', 'transition-timing-function': 'ease-in-out'});
  }, 10);
}

function rainbow(elt) {
  "use strict";
  console.log("RAINBOW");
  tempHighlight(elt, {color: 'inherit', duration: '1s', next: 'red'});
    setTimeout(function () {tempHighlight(elt, {color: 'red', duration: '1s', next: 'orange'});
      setTimeout(function () {tempHighlight(elt, {color: 'orange', duration: '1s', next: 'yellow'});
        setTimeout(function () {tempHighlight(elt, {color: 'yellow', duration: '1s', next: 'green'});
          setTimeout(function () {tempHighlight(elt, {color: 'green', duration: '1s', next: 'blue'});
            setTimeout(function () {tempHighlight(elt, {color: 'blue', duration: '1s', next: 'violet'});
              setTimeout(function () {tempHighlight(elt, {color: 'violet', duration: '1s', next: 'inherit'});
                }, 800);
              }, 800);
            }, 800);
          }, 800);
        }, 800);
      }, 800);
}

function getCoords(cell) {
  "use strict";
  return cell.attr('id').split("-");
}

function getCoords(cell) {
  "use strict";
  return cell.attr('id').split("-");
}

function getCell(coords) {
  "use strict";
  var id = coords.join("-");
  return $("#" + id);
}

function copyMatrix(arr) {
  "use strict";
  var result = [],
    x,
    y;
  for (y = 0; y < arr.length; y += 1) {
    r = [];
    for (x = 0; x < arr[0].length; x += 1) {
      r.push(arr[y][x]);
    }
    result.push(r);
  }
  return result;
}

function isValidDigit(c) {
  "use strict";
  return digits.indexOf(c) !== -1;
}

partialSolution = copyMatrix(clueSet);

function redrawBoard() {
  "use strict";
  var x, y, cell;
  for (x = 0; x < partialSolution.length; x += 1) {
    for (y = 0; y < partialSolution.length; y += 1) {
      cell = getCell([x, y]);
      cell.text(partialSolution[y][x]);
    }
  }
}

function getNumber(cell) {
  "use strict";
  var coords = getCoords(cell),
    x = coords[0],
    y = coords[1];
  cell.on('keypress', function (c) {
    var value = parseInt(c.key, 10);
    if (isValidDigit(value)) {
      partialSolution[y][x] = value;
      if (partialSolution.toString() === solution.toString()) {
        console.log("WHEEEE");
        rainbow($('.square'));
      }
      redrawBoard();
    }
  });
}

function clear(cell) {
  "use strict";
  var coords = getCoords(cell),
    x = coords[0],
    y = coords[1];
  partialSolution[y][x] = null;
  redrawBoard();
}

function hint() {
  "use strict";
  var emptyCells = $.find('.square').filter(function (cell) {
    var empty = $(cell).text() === '';
    return empty;
  }),
    cell = chooseRandomFromArr(emptyCells),
    coords,
    x,
    y;
  if (cell) {
    coords = getCoords($(cell));
    x = coords[0];
    y = coords[1];
    partialSolution[y][x] = solution[y][x];
    tempHighlight($(cell));
    redrawBoard();
  }
}

$('.free').on('focus', function () {
  "use strict";
  getNumber($(this));
});

$('.free').on('contextmenu', function () {
  "use strict";
  clear($(this));
});

$('#clear').on('click', function () { // also occurs on submitting via enter
  "use strict";
  partialSolution = copyMatrix(clueSet);
  redrawBoard();
});

$('#hint').on('click', hint);
