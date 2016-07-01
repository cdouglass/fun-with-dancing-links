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
  elt.css({'background-color': options.color, 'transition-property': 'background-color', 'transition-duration': '0s'});
  setTimeout(function () {
    elt.css({'background-color': options.next, 'transition-property': 'background-color', 'transition-duration': options.duration});
  }, 10);
}

function rainbow(elt) {
  "use strict";
  var hue = 0;
  function makeColor(h) {
    return 'hsl(' + h + ', 100%, 50%)';
  }
  function nextColor() {
    var inc = 32;
    hue += inc;
    tempHighlight(elt, {color: makeColor(hue - inc), duration: '1s', next: makeColor(hue)});
  }
  nextColor();
  setTimeout(function () { nextColor();
    setTimeout(function () { nextColor();
      setTimeout(function () { nextColor();
        setTimeout(function () { nextColor();
          setTimeout(function () { nextColor();
              setTimeout(function () { nextColor();
                setTimeout(function () { nextColor();
                  setTimeout(function () { nextColor();
                  }, 1000);
                }, 1000);
              }, 1000);
            }, 1000);
          }, 1000);
        }, 1000);
      }, 1000);
    }, 1000);
}

function getCoords(cell) {
  "use strict";
  var digits = cell.attr('id').split("-");
  return digits.map(function (x) { return parseInt(x, 10); });
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
}).on('keydown', function (e) {
  "use strict";
  if (e.keyCode === 32) {
    clear($(this));
  }
});

$('#clear').on('click', function () { // also occurs on submitting via enter
  "use strict";
  partialSolution = copyMatrix(clueSet);
  redrawBoard();
});

$('#hint').on('click', hint);
$('.square').keydown(function (e) {
  "use strict";
  var elt = $(document.activeElement),
    x = 0,
    y = 0;
  if (elt.hasClass('square')) {
    [x, y] = getCoords($(document.activeElement));
    switch (e.keyCode) {
    case 37: // left
    case 72: // h (fallthrough)
      x -= 1;
      break;
    case 38: // up
    case 75: // k
      y -= 1;
      break;
    case 39: // right
    case 76: // l
      x += 1;
      break;
    case 40: // down
    case 74: // j
      y += 1;
      break;
    }
    $(getCell([x, y])).focus();
  }
});
