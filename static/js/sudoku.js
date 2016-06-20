/*jslint browser: true, indent:2*/
/*global $, clueSet*/
var board = $("#board"),
  digits = [1, 2, 3, 4, 5, 6, 7, 8, 9],
  currentSolution,
  r;

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

function isValidUnit(arr) {
  "use strict";
  var digitIndices = {}; // TODO empty arr for each digit, add indices, if any digit has >1 index do something
}

currentSolution = copyMatrix(clueSet);

function redrawBoard() {
  "use strict";
  var x, y, cell;
  for (x = 0; x < currentSolution.length; x += 1) {
    for (y = 0; y < currentSolution.length; y += 1) {
      cell = getCell([x, y]);
      cell.text(currentSolution[y][x]);
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
      currentSolution[y][x] = value;
      redrawBoard();
    }
  });
}

function clear(cell) {
  "use strict";
  var coords = getCoords(cell),
    x = coords[0],
    y = coords[1];
  currentSolution[y][x] = null;
  redrawBoard();
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
  currentSolution = copyMatrix(clueSet);
  redrawBoard();
});
