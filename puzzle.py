import os
import flask
import time # TODO remove
from celery import Celery
import lib.n_queens

app = flask.Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'amqp://guest@localhost//'

celery = Celery(app.name, backend="rpc://", broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task
def solve_n_queens_in_background(n):
  return lib.n_queens.n_queens(n)

# use decorator to link a function to a url
@app.route('/')
def hello():
  return flask.redirect('/n_queens')

@app.route('/n_queens', methods=['GET', 'POST'])
def n_queens():
  n = 4 if flask.request.method == 'GET' else int(flask.request.form['board_size'])
  if n < 5: # TODO don't have hard-coded cutoff (but if no better idea, change it to 12 in prod)
    solutions = lib.n_queens.n_queens(n)
  else:
    task = solve_n_queens_in_background.delay(n)
    while not(task.result):
      time.sleep(0.1) # TODO this still needs to be moved OUT of the request or heroku will time it out
    solutions = task.result
  return flask.render_template('n_queens.html', solutions = solutions, n = n)

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(port=port)
