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
  n = int(flask.request.form['board_size']) if flask.request.form else 4
  solutions = lib.n_queens.n_queens(n) if flask.request.method == 'GET' else []
  return flask.render_template('n_queens.html', solutions = solutions, n = n)

@app.route('/n_queens_solutions_only', methods=['POST'])
def n_queens_solutions_only():
  n = int(flask.request.form['board_size'])
  task = solve_n_queens_in_background.delay(n)
  return flask.jsonify(Location=flask.url_for('n_queens_task'), task_id=task.id), 200

@app.route('/n_queens_task')
def n_queens_task():
  task_id = flask.request.args.get('task_id')
  task = solve_n_queens_in_background.AsyncResult(task_id)
  response = {}
  if task.state != 'PENDING':
    response['result'] = task.result
  else:
    response['result'] = {'status': 'PENDING'}
  return flask.jsonify(response)

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(port=port)
