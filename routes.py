import sqlite3
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
    return render_template(
      'home.html',
      title = 'Home')

#agents route to get names from database
@app.route('/agents/')
def agent():
    conn = sqlite3.connect('12Valorant.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Agents')
    results = cursor.fetchall()
    conn.close()
    return render_template('agents.html', results = results, title = 'Agents')

#
@app.route('/agents/<int:id>')
def agentid(id):
    conn = sqlite3.connect('12Valorant.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Agents WHERE id = ?;'(id,))
    agentid = cursor.fetchall()
    conn.close()
    return render_template('agentid.html', agentid = agentid, title = 'Agent')


if __name__ == "__main__":
    app.run(port=8080, debug=True)
