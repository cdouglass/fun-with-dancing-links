import lib.my_math
import lib.n_queens
from flask import Flask, render_template, request
app = Flask(__name__)

# use decorator to link a function to a url
@app.route('/')
def hello():
  return "Hello, World!"

@app.route('/n_queens', methods=['GET', 'POST'])
def n_queens():
  if request.method == 'GET':
    return render_template('n_queens_form.html')
  else:
    n = int(request.form['count'])
    result = lib.n_queens.n_queens(n)
    return render_template('n_queens_result.html', result=result)

@app.route('/square', methods=['GET', 'POST'])
def square():
  if request.method == 'GET':
    return render_template('square_form.html')
  else:
    num = int(request.form['argument'])
    result = lib.my_math.square(num)
    return render_template('square_result.html', result=result)

if __name__ == "__main__":
  app.run(debug=True) # TODO turn off debug in production!
