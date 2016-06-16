import os
import flask
from flask import request
from celery import Celery
import lib.n_queens

app = flask.Flask(__name__)
# changed from .get("thingy") to ["thingy"] at same time as CLOUDAMQP -> REDIS_URL
app.config['CELERY_BROKER_URL'] = os.environ.get("CLOUDAMQP_URL")
app.config['CELERY_RESULT_BACKEND'] = os.environ.get("CLOUDAMQP_URL")
app.config['CELERY_IGNORE_RESULT'] = False
if os.path.exists('config.py'):
  app.config.from_pyfile('config.py')

celery = Celery(app.name, backend=['CELERY_RESULT_BACKEND'], broker=app.config['CELERY_BROKER_URL'], BROKER_POOL_LIMIT=3)
celery.conf.update(app.config)

@celery.task
def solve_n_queens_in_background(n):
  return lib.n_queens.n_queens(n)

@app.route('/')
def index():
  return flask.render_template('index.html')

@app.route('/n_queens')
def n_queens_default():
  args = request.args
  n = int(args['n']) if args else 8
  solutions = lib.n_queens.n_queens(n)
  return flask.render_template('n_queens.html', solutions = solutions, n = n)

@app.route('/n_queens_board_only')
def n_queens_board_only():
  n = int(request.args['n'])
  return flask.render_template('n_queens_container.html', solutions = [], n = n)

@app.route('/n_queens_solutions_only')
def n_queens_solutions_only():
  n = int(request.args['n'])
  task = solve_n_queens_in_background.delay(n)
  return flask.jsonify(Location=flask.url_for('n_queens_background_task'), task_id=task.id), 200

@app.route('/n_queens_task')
def n_queens_background_task():
  task_id = request.args.get('task_id')
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
