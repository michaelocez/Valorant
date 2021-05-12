import sqlite3
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def home():
    return render_template(
      'home.html',
      title = 'Home')

@app.route('/agents')
def agents():
    return render_template(
      'agents.html',
      title = 'Agents')

if __name__ == "__main__":
    app.run(port=8080, debug=True)
