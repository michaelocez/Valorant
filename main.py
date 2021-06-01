import sqlite3
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
    return render_template(
      'home.html',
      title = 'Home')

@app.route('/agents/')
def agents():
    conn = sqlite3.connect('12Valorant.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM Agents')
    results = cursor.fetchall()
    conn.close()
    return render_template('agents.html', results = results)

if __name__ == "__main__":
    app.run(port=8080, debug=True)
