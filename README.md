#Fun with dancing links

##About

This project is a demonstration of the use of the dancing links method of solving exact cover problems, such as Sudoku and the [N queens problem](https://en.wikipedia.org/wiki/Eight_queens_puzzle). It is currently online at [https://secret-thicket-64664.herokuapp.com/](https://secret-thicket-64664.herokuapp.com/).

So far only the N queens portion of the project is complete.

###Context: Exact cover problems

These are problems where the goal is to find a solution satisfying each one of a set of conditions exactly once. Sudoku is an example that's easy to visualize: each row, column, and sub-grid must contain exactly one of each digit from 1 through 9. Solving problems of this form, as far as we know, has a time requirement that's exponential in the size of the input.

The obvious way to find all solutions to such a problem is performing a depth-first search using backtracking; the dancing links technique uses a nifty data structure that makes backtracking more efficient. A paper describing its use, with several examples, is available at [arxiv.org](http://arxiv.org/abs/cs/0011047).

The N queens problem is not strictly an exact cover problem, since each diagonal may contain either one or zero queens. This can be handled with a slight change to the data structure involved so that the program will not waste time trying to cover diagonals.

##Setup (for Debian-based Linuxes; not tested elsewhere)

###Initial setup

```
$ sudo apt-get install python3
$ sudo apt-get install python3-pip
$ sudo apt-get install python3-venv
$ sudo apt-get install rabbitmq-server
```
###Running the site:

Navigate to project root directory, then run
```
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
$ python3 -m puzzle
$ celery --app=puzzle.celery worker --loglevel=info
```
Site will be running at [http://localhost:5000](http://localhost:5000).

###Running the tests:

```
$ python3 -m tests
```
