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
  return c in [1, 2, 3, 4, 5, 6, 7, 8, 9]
}

function isValidUnit(arr) {
  // TODO
}

function redrawBoard(values) {
  var x, y, square;
  for (x = 0; x < values.length; x++) {
    for (y = 0; y < values.length; y++) {
      square = getSquare([x, y]);
      square.text(values[y][x]);
    }
  }
}

function getNumber(square) {
  var [x, y] = getCoords(square);
  square.on('keypress', function(c) {
    var value = c.key;
    if (isValidDigit(value)) {
      currentSolution[y][x] = value;
      redrawBoard(currentSolution);
    }
  });
}

$('.free').on('focus', function() {
  getNumber($(this));
});
