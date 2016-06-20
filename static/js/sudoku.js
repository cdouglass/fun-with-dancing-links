// global clueSet
var board = $("#board");

function getCoords(square) {
  return square.attr('id').split("-");
}

function getSquare(coords) {
  var id = coords.join("-");
  return $("#" + id);
}

function copyMatrix(arr) {
  var result = [];
  for (y = 0; y < arr.length; y++) {
    r = []
    for (x = 0; x < arr[0].length; x++) {
      r.push(arr[y][x]);
    }
    result.push(r);
  }
  return result;
}

var currentSolution = copyMatrix(clueSet),
  r;

function isValidDigit(c) {
  return [1, 2, 3, 4, 5, 6, 7, 8, 9].indexOf(c) != -1;
}

function isValidUnit(arr) {
  // TODO
}

function redrawBoard() {
  var x, y, square;
  for (x = 0; x < currentSolution.length; x++) {
    for (y = 0; y < currentSolution.length; y++) {
      square = getSquare([x, y]);
      square.text(currentSolution[y][x]);
    }
  }
}

function getNumber(square) {
  var [x, y] = getCoords(square);
  square.on('keypress', function(c) {
    var value = parseInt(c.key);
    if (isValidDigit(value)) {
      currentSolution[y][x] = value;
      redrawBoard();
    }
  });
}

function clear(square) {
  var [x, y] = getCoords(square);
  currentSolution[y][x] = null;
  redrawBoard();
}

$('.free').on('focus', function() {
  getNumber($(this));
});

$('.free').on('contextmenu', function() {
  clear($(this));
});

$('#clear').on('click', function() { // also occurs on submitting via enter
  currentSolution = copyMatrix(clueSet);
  redrawBoard();
});
