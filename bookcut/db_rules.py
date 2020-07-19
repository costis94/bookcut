import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None;
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_book(conn, book):
    sql = ''' INSERT OR IGNORE INTO books(bookname,authorname,publisher,file)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, book)
    conn.commit()
    return cur.lastrowid



def main(a,b,c,d):
    database = "bookdb.db"

    sql_create_books_table = """ CREATE TABLE IF NOT EXISTS books (
                                        id integer PRIMARY KEY,
                                        bookname text NOT NULL,
                                        authorname text NOT NULL,
                                        publisher text,
                                        file integer
                                    ); """

    # create a database connection
    conn = create_connection(database)
    cur = conn.cursor()

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_books_table)
    else:
        print("Error! cannot create the database connection.")


    #ELEGXOS DIPLOTYPWN
    cur.execute("""SELECT bookname,authorname FROM books WHERE bookname=? AND authorname=?""",(a,b))
    result = cur.fetchone()

    if result:
        #print("The book " + a + " by " + b +"=========== Already exists")
        pass
    else:
        with conn:
            book = (a,b,c,0)
            book_id = create_book(conn,book)
            print(a,b,c)

def updater(a,b,d):
    database = "bookdb.db"
    conn = create_connection(database)
    cur = conn.cursor()
    sqql = ''' UPDATE books SET file=1 WHERE bookname=? AND authorname=?'''
    cur.execute(sqql, (a,b))
    conn.commit()
    #print("Record Updated successfully ")
    cur.close()

def file_checker(a,b):
    database = "bookdb.db"
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute("""SELECT bookname,authorname FROM books WHERE bookname=? AND authorname=? AND file=1""",(a,b))
    result = cur.fetchone()
    if result:
        return True
    else:
        return False

if __name__ == '__main__':
    main()
