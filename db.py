import sqlite3

def connection():
    try:
        con=sqlite3.connect(database="bank.sqlite")
        cur=con.cursor()
        table1="create table accounts(username  text primary key,password text,email text,contact float);"
        table2="create table txn(username text,date text,item float,item_name text);"
        cur.execute(table2)
        cur.execute(table1)
        con.commit()
        con.close()  
        return ("Tables created")
    except:
        return ("something went wrong in db,might be tabl(s) already exists")
