import sqlite3
from flask import Flask, render_template
app = Flask(__name__)

#DEBUG working on do query
def do_query(query,data= None,fetchall=False):
    conn = sqlite3.connect('12Valorant.db')
    cursor = conn.cursor()
    if data is None:
        cursor.execute(query)
    else:
        cursor.execute(query,data)
    results = cursor.fetchall() if fetchall else cur.fetchall()
    return results

#home page
@app.route('/')
def home():
    return render_template('home.html',title = 'Home')

#agents route to get names from database
@app.route('/agents/')
def agent():
    agents = do_query('SELECT * FROM Agents', data = None, fetchall = True)
    return render_template('agents.html', agents = agents, title = 'Agents')

#page for each agent
@app.route('/agents/<int:id>')
def agentid(id):
    agentid = do_query('SELECT Agents.*, Weapon.name FROM Agents JOIN Weapon on Agents.carrying_weapon = Weapon.id WHERE Agents.id = ?;',(id,),fetchall = True)
    return render_template('agentid.html', agentid = agentid, title = 'Agent')

#page to get all weapons
@app.route('/weapons/')
def weapons():
    weapons = do_query('SELECT * FROM Weapon', data = None, fetchall = True)
    return render_template('weapons.html', weapons = weapons, title = 'Weapons')

@app.route('/weapons/<int:id>')
def weaponid(id):
    weaponid = do_query('SELECT * FROM Weapon WHERE Weapon.id = ?',(id,), fetchall = True)
    return render_template('weaponid.html', weaponid = weaponid, title = 'Weapon')

@app.route('/skins/')
def skincollection():
    skincollection = do_query('SELECT * FROM SkinCollection', data = None, fetchall = True)
    return render_template('skincollection.html', skincollection = skincollection, title= 'Skins')

@app.route('/skins/<int:id>')
def skinscollectionid(id):
    skincollectionid = do_query('SELECT * FROM SkinCollection WHERE SkinCollection.id = ?',(id,), fetchall = True)
    return render_template('skincollectionid.html', skincollectionid = skincollectionid, title= 'Skins')

if __name__ == "__main__":
    app.run(port=8080, debug=True)
