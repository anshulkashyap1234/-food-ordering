from flask import Flask, render_template, request, redirect, url_for, flash
import os
import random
import sqlite3
import db
from datetime import datetime
import re
app = Flask(__name__)
database = db.connection()
print(database)


@app.route('/')
def home():
    return render_template("/before login/rest.html")


@app.route('/loginbutton')
def loginbutton():
    return render_template("/before login/login.html")


@app.route('/create_account')
def create_account():
    return render_template("/before login/create_account.html")


# loginform
@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        print(username, password)

        if (username == "" or password == ""):
            return render_template('/before login/login.html', error="invalid username and password")
        else:
            # connect form to sql

            con = sqlite3.connect(database="bank.sqlite")
            cur = con.cursor()
            cur.execute(
                "select * from accounts where username=? and password=?", (username, password))
            global tup
            tup = cur.fetchone()
            if (tup == None):
                return render_template('/before login/login.html', error="invalid username and password")
            else:
                con = sqlite3.connect(database="bank.sqlite")
                cur = con.cursor()
                cur.execute("select * from txn where username=?;",(tup[0],))
                tup1 = cur.fetchall()
                con.close()
                return render_template('/after login/items.html', username=tup[0],item_no=len(tup1))


@app.route('/account_open', methods=['POST', 'GET'])
def account_open():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        email = request.form['email']
        contact = request.form['contact_no']

        if username == "" or password == "" or email == "" or contact == "":
            return render_template("/before login/create_account.html", error="invalid data")
        else:
            try:
                con = sqlite3.connect(database="bank.sqlite")
                cur = con.cursor()
                cur.execute("insert into accounts(username,password,email,contact) values(?,?,?,?)",
                            (username, password, email, contact))
                con.commit()
                con.close()
                return render_template("before login/create_account.html", error="account created")
            except:
                return render_template("before login/create_account.html", error="usename already exsist")




@app.route('/logout')
def logout():
    return render_template("/before login/rest.html")
@app.route('/items')
def items():
                con = sqlite3.connect(database="bank.sqlite")
                cur = con.cursor()
                cur.execute("select * from txn where username=?;",(tup[0],))
                tup1 = cur.fetchall()
                con.close()
                return render_template('/after login/items.html', username=tup[0],item_no=len(tup1))




@app.route('/list', methods=['POST'])
def list():
    data = request.form['price']
    

    date = str(datetime.now())

    data=str(data)
    x=re.findall(r'\d',data)
    item_price=""
    for i in x:
        item_price=item_price+i+""
    item_name=re.findall(r'[a-z]+',data)


    item_price=int(item_price)
    




    con = sqlite3.connect(database="bank.sqlite")
    cur = con.cursor()
    cur.execute("insert into txn(username,date,item,item_name) values(?,?,?,?)",(tup[0], date, item_price, item_name[0]))
    con.commit()
    con.close()
   
    con = sqlite3.connect(database="bank.sqlite")
    cur = con.cursor()
    cur.execute("select * from txn where username=?;",(tup[0],))
    tup1 = cur.fetchall()
    con.close()

    return render_template('/after login/items.html', username=tup[0],item_no=len(tup1))


@app.route('/cart')
def cart():
    

  
    con = sqlite3.connect(database="bank.sqlite")
    cur = con.cursor()
    cur.execute("select sum(item) from txn where  username=?;",(tup[0],))
    total = cur.fetchone()
    con.close()

    con = sqlite3.connect(database="bank.sqlite")
    cur = con.cursor()
    cur.execute("select * from txn where username=?;",(tup[0],))
    tup1 = cur.fetchall()
    con.close()

    return render_template("/after login/bill.html", txn=tup1, total=total[0],username=tup[0],item_no=len(tup1))


@app.route('/delete', methods=['POST'])
def delete():
    delete = request.form['delete']

    con = sqlite3.connect(database="bank.sqlite")
    cur = con.cursor()
    cur.execute("DELETE FROM txn WHERE date=?", (delete,))
    con.commit()
    con.close()

    return redirect(url_for("cart"))


if __name__ == "__main__":
    app.run(debug=True)
