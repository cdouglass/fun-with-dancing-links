#Fun with dancing links

##About

This project is a demonstration of the use of the dancing links technique, a cute method of solving exact cover problems including Sudoku and the [N queens problem](https://en.wikipedia.org/wiki/Eight_queens_puzzle). It is currently online at [https://secret-thicket-64664.herokuapp.com/](https://secret-thicket-64664.herokuapp.com/).

###Context: Exact cover problems

These are problems where the goal is to find a solution satisfying each one of a set of conditions exactly once. The obvious way to find all solutions to such a problem is performing a brute-force search using backtracking. Since the exact cover problem is NP-complete, as far as we know it takes time exponential in the size of the input to solve deterministically, so there's no approach that's substantially more efficient than backtracking. The dancing links technique doesn't overcome this, but it uses a nifty data structure that makes it very convenient to undo an attempted move without needing to copy any saved state. Knuth's paper describing its use, with several examples, is available at [arxiv.org](http://arxiv.org/abs/cs/0011047).

The N queens problem is not strictly an exact cover problem, since each diagonal may contain either one or zero queens, but this can be handled with a slight change to the data structure involved to allow some constraints to be satisfied at most once instead of exactly once.

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
