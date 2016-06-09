Initial setup for Debian-based Linuxes:
```
sudo apt-get install python3
sudo apt-get install python3-pip
sudo apt-get install python3-venv
sudo apt-get install rabbitmq-server
```

Running the site:

Navigate to project root directory, then run
```
python3 -m venv env
source env/bin/activate
python3 -m puzzle
celery --app=puzzle.celery worker --loglevel=info
```
Site will be running at http://localhost:5000.

Running the tests:
```
$ python3 -m tests
```

Try it online at [https://secret-thicket-64664.herokuapp.com/](https://secret-thicket-64664.herokuapp.com/).
