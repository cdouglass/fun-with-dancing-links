import os
import flask
import lib.n_queens
app = flask.Flask(__name__)

# use decorator to link a function to a url
@app.route('/')
def hello():
  return flask.redirect('/n_queens')

@app.route('/n_queens', methods=['GET', 'POST'])
def n_queens():
  n = 2 if flask.request.method == 'GET' else int(flask.request.form['board_size'])
  solutions = lib.n_queens.n_queens(n)
  return flask.render_template('n_queens.html', solutions = solutions, n = n)

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(port=port)
