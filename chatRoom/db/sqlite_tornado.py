import sqlite3

def get_db():
    conn=sqlite3.connect('test_tornado_db')
    cur=conn.cursor()
    return cur

def db_init():
    conn=sqlite3.connect("test_tornado_db")
    cur=conn.cursor()
    cur.execute("select count(*) from sqlite_master where type='table' and name='user_table'")
    b=cur.fetchall()
    if b[0][0]==1:
            pass
    else:
            cur.execute("create table user_table (user_id integer PRIMARY KEY AUTOINCREMENT ,user_name varchar(20),user_passwd varchar(20),mailNum varchar(30))")
            cur.execute("insert into user_table values(?,?,?,?)",(None,'admin','admin','850230720@qq.com'))
            conn.commit()
    conn.close()


