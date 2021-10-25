# tells python to use flask module and other things
# I need such as sqlite3 for database integration

import sqlite3
from flask import Flask, render_template, request, redirect, flash, abort

app = Flask(__name__)
app.secret_key = "18197"


# do query to avoid repeated code when using @app.route
def do_query(query, data=None, fetchall=False):
    conn = sqlite3.connect('12Valorant.db')  # connects to database file
    cursor = conn.cursor()  # assigns the connections cursor
    if data is None:
        cursor.execute(query)
    else:
        cursor.execute(query, data)
    results = cursor.fetchall() if fetchall else cursor.fetchone()
    return results


# Creates a route for the flaskapp for the home route
@app.route('/')
def home():
    # queries to get my favourite agent,weapon and skins
    homea = do_query('SELECT * FROM Agents WHERE id = 11')
    homew = do_query('SELECT * FROM Weapon WHERE id = 16')
    homes = do_query('''SELECT Skin.*, SkinCollection.*, Weapon.name
                     FROM Skin JOIN SkinCollection
                     on Skin.collection = SkinCollection.id
                     JOIN Weapon ON Weapon.id = Skin.weapon
                     WHERE Skin.id = 30''', fetchall=True)
    return render_template('home.html', homea=homea, homew=homew,
                           homes=homes, title='Home')
# return the render template function to the user
# so that they can see the html file and add the title home to the tab


# route to get everything from agents table
# presents all the names and images on one page
@app.route('/agents/')
def agent():
    agents = do_query('SELECT * FROM Agents', fetchall=True)
    return render_template('agents.html', agents=agents, title='Agents')


# route to get each agents data including weapon the weapon
# from selected id to show on each page
@app.route('/agents/<int:id>')
def agent_id(id):
    # query shows all data from picked agents table
    # and shows their carrying weapon
    agent_id = do_query('''SELECT Agents.*, Weapon.name FROM Agents
                       JOIN Weapon on Agents.carrying_weapon = Weapon.id
                       WHERE Agents.id = ?;''', (id,), fetchall=True)
    if len(agent_id) == 0:
        abort(404)  # sending user to error page due to manual URL change
    return render_template('agentid.html', agent_id=agent_id, title='Agent')


# route grabs all data from weapons table and shows the image and name on page
@app.route('/weapons/')
def weapons():
    weapons = do_query('SELECT * FROM Weapon', fetchall=True)
    return render_template('weapons.html', weapons=weapons, title='Weapons')


# route takes data from selected id in weapons table
# presents its name, image and description of weapon
@app.route('/weapons/<int:id>')
def weapon_id(id):
    # query shows all data from weapons table from the picked weapon
    weapon_id = do_query('SELECT * FROM Weapon WHERE Weapon.id = ?',
                        (id,), fetchall=True)
    if len(weapon_id) == 0:
        abort(404)  # sending user to error page due to manual URL change
    return render_template('weaponid.html', weapon_id=weapon_id,
                           title='Weapon')


# route gets all data from skincollection table
# presents all names and images on one webpage
@app.route('/skins/')
def skin_collection():
    # query shows skin collection image and name
    skin_collection = do_query('SELECT * FROM SkinCollection', fetchall=True)
    return render_template('skincollection.html',
                           skin_collection=skin_collection, title='Skins')


# route gets skin collection name, image all skins and weapons
# linked to selected id of skin collection
@app.route('/skins/<int:id>')
def skins(id):
    # query shows all skins from the picked skin collection
    # links weapon to each skin
    skins = do_query('''SELECT Skin.*, SkinCollection.*,
                      Weapon.name FROM Skin JOIN SkinCollection
                      on Skin.collection = SkinCollection.id
                      JOIN Weapon ON Weapon.id = Skin.weapon
                      WHERE Skin.collection = ?''', (id,), fetchall=True)
    if len(skins) == 0:
        abort(404)  # sending user to error page due to manual URL change
    return render_template('skins.html', skins=skins, title='Skins')


# route for search bar to search skin collection
@app.route('/search', methods=["POST", "GET"])
def search():
    if request.method == "POST":
        print (request.form.get("filter"))
        # query takes user input and sends them to the skin collection
        # with the same first letter
        search = do_query('''SELECT * FROM SkinCollection
                          WHERE SkinCollection.visible_name
                          LIKE "" || ? || "%"
                          ORDER BY SkinCollection.visible_name;''',
                          (request.form.get("filter"),), fetchall=True)
        # query selects all from skin collection table
        if len(search) == 0:
            abort(404)  # if input has 0 characters, it will abort to 404 page
        if request.form.get("filter") == '':
            abort(404)  # fix for when user presses enter
        else:
            return redirect(f'/skins/{(search[0])[0]}')
            # sends user to searched page


# page with no database interaction
# just displays html and css from the contact.html page
@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')


# form for user to fill in name,email and message
@app.route("/message", methods=["POST"])
def message():
    # allows user to input their name, email and message as contact.
    connection = sqlite3.connect('12Valorant.db')
    cursor = connection.cursor()
    # using forms to get user input
    user_first_name = request.form["user_first_name"]
    user_last_name = request.form["user_last_name"]
    user_email = request.form["user_email"]
    user_message = request.form["user_message"]
    # query gets user input and inserts into respective column in contact table
    sql = '''INSERT INTO contact(user_first_name, user_last_name,
        user_email, user_message) VALUES (?, ?, ?, ?)'''
    cursor.execute(sql, (user_first_name, user_last_name,
                   user_email, user_message))
    flash('Thank you!')  # shows message after sending a message
    connection.commit()
    connection.close()
    return redirect('/contact')


# gives user an error when URL entered doesn't go to a route on the site
@app.errorhandler(404)
def error404(error):
    return render_template('404.html', title='Error'), 404
    # returns the 404 page


# runs site on local port 8080
if __name__ == "__main__":
    app.run(port=8080, debug=True)
