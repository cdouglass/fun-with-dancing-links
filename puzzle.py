import lib.n_queens
import flask
app = flask.Flask(__name__)

# use decorator to link a function to a url
@app.route('/')
def hello():
  return flask.redirect('/n_queens')

@app.route('/n_queens', methods=['GET', 'POST'])
def n_queens():
  if flask.request.method == 'GET':
    solutions = []
  else:
    n = int(flask.request.form['count'])
    solutions = lib.n_queens.n_queens(n)
  return flask.render_template('n_queens.html', solutions=solutions)

if __name__ == "__main__":
  app.run()
