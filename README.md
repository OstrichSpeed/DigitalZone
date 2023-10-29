# Digital Zone (flask-ecomm)
An eCommerce App built with Flask, Jinja, SQLite, jQuery and Bootstrap

The app loads a gallery of digital and home appliances that includes: image, description, price, and a small form to add item to cart. The product info is stored in a SQLite database and is displayed using Bootstrap's card class.

The app includes a series of filters implemented using SQLite queries so you can see only product that match a certain filter: manufacturers, categories, products on sale, etc.

If a user is not logged in and tries to add something to the shopping cart she will see a warning message (implemented with jQuery) asking her to log in.

Once registered and logged in, the user can add products to the shopping cart. A link to the shopping cart can be found at the top right of the screen, showing the amount of items in the cart as well as the sub-total in dollars. Clicking the shopping cart link opens a Bootstrap modal window showing the shopping cart in more detail. 

If you want to make changes, like add one more product or remove a product, you can click on the Make Changes button and you will be taken to the full version of the shopping cart.

Once you check out, the idea is to be sent to a payment processor. However, that part is not implemented yet.

If you want to see your purchase history, just click on the You Bought link and you will see all the products you have ever bought. You will also find a Buy Again link that will direct you to the product page in case you want to buy it again.

Once you're finished, you can just log out.

If you want to see the app in action, fork the repository to your own computer and perform the following commands from the command line in your project folder:

<code>export FLASK_APP=application.py</code><br />
<code>flask run</code>

This assumes you have Python, Flask and SQLite installed in your computer, as well as a link to Bootstrap and the following modules necessary to run application.py installed:

<code>
from cs50 import SQL</code><br />
<code>from flask_session import Session</code><br />
<code>from flask import Flask, render_template, redirect, request, session, jsonify</code><br />
<code>from datetime import datetime</code>

