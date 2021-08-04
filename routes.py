import sqlite3
from flask import Flask, render_template, request, redirect
app = Flask(__name__)

#Do Query to avoid repeated code when using @app.route
def do_query(query,data= None,fetchall=False):
    conn = sqlite3.connect('12Valorant.db')
    cursor = conn.cursor()
    if data is None:
        cursor.execute(query)
    else:
        cursor.execute(query,data)
    results = cursor.fetchall() if fetchall else cursor.fetchall()
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

#route for page to show each agent
@app.route('/agents/<int:id>')
def agentid(id):
    agentid = do_query('SELECT Agents.*, Weapon.name FROM Agents JOIN Weapon on Agents.carrying_weapon = Weapon.id WHERE Agents.id = ?;',(id,),fetchall = True)
    return render_template('agentid.html', agentid = agentid, title = 'Agent')

#route to show all weapons on one page
@app.route('/weapons/')
def weapons():
    weapons = do_query('SELECT * FROM Weapon', data = None, fetchall = True)
    return render_template('weapons.html', weapons = weapons, title = 'Weapons')

#route to show each weapon on its own page
@app.route('/weapons/<int:id>')
def weaponid(id):
    weaponid = do_query('SELECT * FROM Weapon WHERE Weapon.id = ?',(id,), fetchall = True)
    return render_template('weaponid.html', weaponid = weaponid, title = 'Weapon')

#route to show all skin collections on a page
@app.route('/skins/')
def skincollection():
    skincollection = do_query('SELECT * FROM SkinCollection', data = None, fetchall = True)
    return render_template('skincollection.html', skincollection = skincollection, title= 'Skins')

#route to show every skin in a skin collection on its own page
@app.route('/skins/<int:id>')
def skins(id):
    skins = do_query('SELECT Skin.*, SkinCollection.*, Weapon.name FROM Skin JOIN SkinCollection on Skin.collection = SkinCollection.id JOIN Weapon ON Weapon.id = Skin.weapon WHERE Skin.collection = ?',(id,), fetchall = True)
    return render_template('skins.html', skins = skins, title= 'Skins')

@app.route ('/search', methods=["POST", "GET"])
def search():
    #search bar
    if request.method == "POST":
        print (request.form.get("filter"))
        search = do_query("SELECT * FROM SkinCollection WHERE SkinCollection.name LIKE '%' || ? || '%' ORDER BY SkinCollection.name;", (request.form.get("filter"),), fetchall = True)
        if len(search) == None:
            return redirect ('/error')
        else:
            return redirect (f"/skins/{(search[0])[0]}")
    return render_template('search.html')

#error page
@app.errorhandler(404)
def error404(error):
    return render_template('error.html', title='Error')

if __name__ == "__main__":
    app.run(port=8080, debug=True)
