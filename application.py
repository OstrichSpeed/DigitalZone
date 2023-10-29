from cs50 import SQL
from flask_session import Session
from flask import Flask, render_template, redirect, request, session, jsonify
from datetime import datetime

# # Instantiate Flask object named app
app = Flask(__name__)

# # Configure sessions
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Creates a connection to the database
db = SQL ( "sqlite:///data.db" )

@app.route("/")
def index():
    items = db.execute("SELECT * FROM items ORDER BY name ASC")
    itemsLen = len(items)
    # Initialize variables
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    if 'user' in session:
        shoppingCart = db.execute("SELECT name, image, SUM(qty), SUM(subTotal), price, id FROM cart WHERE uid=:uid GROUP BY name", uid=session["uid"])
        shopLen = len(shoppingCart)
        for i in range(shopLen):
            total += shoppingCart[i]["SUM(subTotal)"]
            totItems += shoppingCart[i]["SUM(qty)"]
        items = db.execute("SELECT * FROM items ORDER BY name ASC")
        itemsLen = len(items)
        return render_template ("index.html", shoppingCart=shoppingCart, items=items, shopLen=shopLen, itemsLen=itemsLen, total=total, totItems=totItems, display=display, session=session )
    return render_template ( "index.html", items=items, shoppingCart=shoppingCart, itemsLen=itemsLen, shopLen=shopLen, total=total, totItems=totItems, display=display)


@app.route("/buy/")
def buy():
    # Initialize shopping cart variables
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    qty = int(request.args.get('quantity'))
    if session:
        # Store id of the selected item
        id = int(request.args.get('id'))
        # Select info of selected item from database
        goods = db.execute("SELECT * FROM items WHERE id=:id", id=id)
        # Extract values from selected item record
        # Check if item is on sale to determine price
        if(goods[0]["onSale"] == 1):
            price = goods[0]["onSalePrice"]
        else:
            price = goods[0]["price"]
        name = goods[0]["name"]
        image = goods[0]["image"]
        subTotal = qty * price
        # Insert selected item into shopping cart
        db.execute("INSERT INTO cart (uid, id, qty, name, image, price, subTotal) VALUES (:uid, :id, :qty, :name, :image, :price, :subTotal)", uid=session["uid"], id=id, qty=qty, name=name, image=image, price=price, subTotal=subTotal)
        shoppingCart = db.execute("SELECT uid, name, image, SUM(qty), SUM(subTotal), price, id FROM cart WHERE uid=:uid GROUP BY name", uid=session["uid"])
        shopLen = len(shoppingCart)
        # Rebuild shopping cart
        for i in range(shopLen):
            total += shoppingCart[i]["SUM(subTotal)"]
            totItems += shoppingCart[i]["SUM(qty)"]
        # Select all items for home page view
        items = db.execute("SELECT * FROM items ORDER BY name ASC")
        itemsLen = len(items)
        # Go back to home page
        return render_template ("index.html", shoppingCart=shoppingCart, items=items, shopLen=shopLen, itemsLen=itemsLen, total=total, totItems=totItems, display=display, session=session )


@app.route("/update/")
def update():
    # Initialize shopping cart variables
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    qty = int(request.args.get('quantity'))
    if session:
        # Store id of the selected item
        id = int(request.args.get('id'))
        db.execute("DELETE FROM cart WHERE uid=:uid and id=:id", uid=session["uid"], id=id)
        # Select info of selected item from database
        goods = db.execute("SELECT * FROM items WHERE id=:id", id=id)
        # Extract values from selected item record
        # Check if item is on sale to determine price
        if(goods[0]["onSale"] == 1):
            price = goods[0]["onSalePrice"]
        else:
            price = goods[0]["price"]
        name = goods[0]["name"]
        image = goods[0]["image"]
        subTotal = qty * price
        # Insert selected item into shopping cart
        db.execute("INSERT INTO cart (uid, id, qty, name, image, price, subTotal) VALUES (:uid, :id, :qty, :name, :image, :price, :subTotal)", uid=session["uid"], id=id, qty=qty, name=name, image=image, price=price, subTotal=subTotal)
        shoppingCart = db.execute("SELECT name, image, SUM(qty), SUM(subTotal), price, id FROM cart WHERE uid=:uid GROUP BY name", uid=session["uid"])
        shopLen = len(shoppingCart)
        # Rebuild shopping cart
        for i in range(shopLen):
            total += shoppingCart[i]["SUM(subTotal)"]
            totItems += shoppingCart[i]["SUM(qty)"]
        # Go back to cart page
        return render_template ("cart.html", shoppingCart=shoppingCart, shopLen=shopLen, total=total, totItems=totItems, display=display, session=session )


@app.route("/filter/")
def filter():
    if request.args.get('manufacturer'):
        query = request.args.get('manufacturer')
        items = db.execute("SELECT * FROM items WHERE manufacturer=:query ORDER BY name ASC", query=query )
    if request.args.get('sale'):
        query = request.args.get('sale')
        items = db.execute("SELECT * FROM items WHERE onSale=:query ORDER BY name ASC", query=query)
    if request.args.get('id'):
        query = int(request.args.get('id'))
        items = db.execute("SELECT * FROM items WHERE id=:query ORDER BY name ASC", query=query)
    if request.args.get('category'):
        query = request.args.get('category')
        items = db.execute("SELECT * FROM items WHERE category=:query ORDER BY name ASC", query=query)
    if request.args.get('price'):
        query = request.args.get('price')
        items = db.execute("SELECT * FROM items ORDER BY onSalePrice ASC")
    itemsLen = len(items)
    # Initialize shopping cart variables
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    if 'user' in session:
        # Rebuild shopping cart
        shoppingCart = db.execute("SELECT name, image, SUM(qty), SUM(subTotal), price, id FROM cart WHERE uid=:uid GROUP BY name", uid=session["uid"])
        shopLen = len(shoppingCart)
        for i in range(shopLen):
            total += shoppingCart[i]["SUM(subTotal)"]
            totItems += shoppingCart[i]["SUM(qty)"]
        # Render filtered view
        return render_template ("index.html", shoppingCart=shoppingCart, items=items, shopLen=shopLen, itemsLen=itemsLen, total=total, totItems=totItems, display=display, session=session )
    # Render filtered view
    return render_template ( "index.html", items=items, shoppingCart=shoppingCart, itemsLen=itemsLen, shopLen=shopLen, total=total, totItems=totItems, display=display)


@app.route("/checkout/")
def checkout():
    order = db.execute("SELECT * from cart WHERE uid=:uid", uid=session["uid"])
    # Update purchase history of current customer
    for item in order:
        db.execute("INSERT INTO purchases (uid, id, name, image, quantity) VALUES(:uid, :id, :name, :image, :quantity)", uid=session["uid"], id=item["id"], name=item["name"], image=item["image"], quantity=item["qty"] )
    # Clear shopping cart
    db.execute("DELETE from cart WHERE uid=:uid", uid=session["uid"])
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    # Redirect to home page
    return redirect('/')


@app.route("/remove/", methods=["GET"])
def remove():
    # Get the id of item selected to be removed
    out = int(request.args.get("id"))
    # Remove item from shopping cart
    db.execute("DELETE from cart WHERE uid=:uid and id=:id", uid=session["uid"], id=out)
    # Initialize shopping cart variables
    totItems, total, display = 0, 0, 0
    # Rebuild shopping cart
    shoppingCart = db.execute("SELECT name, image, SUM(qty), SUM(subTotal), price, id FROM cart WHERE uid=:uid GROUP BY name", uid=session["uid"])
    shopLen = len(shoppingCart)
    for i in range(shopLen):
        total += shoppingCart[i]["SUM(subTotal)"]
        totItems += shoppingCart[i]["SUM(qty)"]
    # Turn on "remove success" flag
    display = 1
    # Render shopping cart
    return render_template ("cart.html", shoppingCart=shoppingCart, shopLen=shopLen, total=total, totItems=totItems, display=display, session=session )


@app.route("/login/", methods=["GET"])
def login():
    return render_template("login.html")


@app.route("/new/", methods=["GET"])
def new():
    # Render log in page
    return render_template("new.html")


@app.route("/logged/", methods=["POST"] )
def logged():
    # Get log in info from log in form
    user = request.form["username"].lower()
    pwd = request.form["password"]
    #pwd = str(sha1(request.form["password"].encode('utf-8')).hexdigest())
    # Make sure form input is not blank and re-render log in page if blank
    if user == "" or pwd == "":
        return render_template ( "login.html" )
    # Find out if info in form matches a record in user database
    query = "SELECT * FROM users WHERE username=:user and password=:pwd"
    rows = db.execute ( query, user=user, pwd=pwd )

    # If username and password match a record in database, set session variables
    if len(rows) == 1:
        session['user'] = user
        session['time'] = datetime.now( )
        session['uid'] = rows[0]["id"]
    # Redirect to Home Page
    if 'user' in session:
        return redirect ( "/" )
    # If username is not in the database return the log in page
    return render_template ( "login.html", msg="Wrong username or password." )


@app.route("/history/")
def history():
    # Initialize shopping cart variables
    shoppingCart = db.execute("SELECT name, image, SUM(qty), SUM(subTotal), price, id FROM cart WHERE uid=:uid GROUP BY name", uid=session["uid"])
    shopLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    # Retrieve all items ever bought by current user
    myItems = db.execute("SELECT * FROM purchases WHERE uid=:uid", uid=session["uid"])
    myItemsLen = len(myItems)
    # Render table with shopping history of current user
    for i in range(shopLen):
        total += shoppingCart[i]["SUM(subTotal)"]
        totItems += shoppingCart[i]["SUM(qty)"]
    return render_template("history.html", shoppingCart=shoppingCart, shopLen=shopLen, total=total, totItems=totItems, display=display, session=session, myItems=myItems, myItemsLen=myItemsLen)


@app.route("/logout/")
def logout():
    # clear shopping cart
    db.execute("DELETE from cart WHERE uid=:uid", uid=session["uid"])
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")


@app.route("/register/", methods=["POST"] )
def registration():
    # Get info from form
    username = request.form["username"]
    password = request.form["password"]
    confirm = request.form["confirm"]
    fname = request.form["fname"]
    lname = request.form["lname"]
    email = request.form["email"]
    # See if username already in the database
    rows = db.execute( "SELECT * FROM users WHERE username=:username ", username = username )
    # If username already exists, alert user
    if len( rows ) > 0:
        return render_template ( "new.html", msg="Username already exists!" )
    # If new user, upload his/her info into the users database
    new = db.execute ( "INSERT INTO users (username, password, fname, lname, email) VALUES (:username, :password, :fname, :lname, :email)",
                    username=username, password=password, fname=fname, lname=lname, email=email )
    # Render login template
    return render_template ( "login.html" )


@app.route("/cart/")
def cart():
    if 'user' in session:
        # Clear shopping cart variables
        totItems, total, display = 0, 0, 0
        # Grab info currently in database
        shoppingCart = db.execute("SELECT name, image, SUM(qty), SUM(subTotal), price, id FROM cart WHERE uid=:uid GROUP BY name", uid=session["uid"])
        # Get variable values
        shopLen = len(shoppingCart)
        for i in range(shopLen):
            total += shoppingCart[i]["SUM(subTotal)"]
            totItems += shoppingCart[i]["SUM(qty)"]
    # Render shopping cart
    return render_template("cart.html", shoppingCart=shoppingCart, shopLen=shopLen, total=total, totItems=totItems, display=display, session=session)


# @app.errorhandler(404)
# def pageNotFound( e ):
#     if 'user' in session:
#         return render_template ( "404.html", session=session )
#     return render_template ( "404.html" ), 404


# Only needed if Flask run is not used to execute the server
if __name__ == "__main__":
   app.run( host='0.0.0.0', port=8080 )
