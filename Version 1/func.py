import sqlite3

# Connecting to the database
conn = sqlite3.connect('com.db')

# Create a cursor
c = conn.cursor()

# Create a table within the database
def create_table():
    c.execute("""CREATE TABLE IF NOT EXISTS parts (
        Material REAL,
        Batch REAL,
        CodeA REAL,
        CodeB REAL,
        CodeC REAL,
        CodeD REAL
    )""")
    conn.commit()

# Inserting just a row of values
def insert_row(materialID, BatchID, CodeA, CodeB, CodeC, CodeD):
    c.execute("INSERT INTO parts VALUES (?, ?, ?, ?, ?, ?)", (materialID, BatchID, CodeA, CodeB, CodeC, CodeD))
    conn.commit()

# Inserting many values/rows into the table
#create an array with the following format remember it goes material ID, Batch Id,
#Code A,B,C,D
many_parts = [
                (6, 7, 8, 9, 10, 11),
                (1.1, 2.2, 3.3, 4.4, 5.5, 6.6),
                (35689.3, 85472.4, 0, 345, 6, 7.8),
            ]
def insert_many(all_parts):
    c.executemany("INSERT INTO parts VALUES (?, ?, ?, ?, ?, ?)", all_parts)
    conn.commit()

# Printing first x rows
def show_many(number_rows):
    c.execute("SELECT * FROM parts")
    rows = c.fetchmany(number_rows)

# Printing all
def show_all():
    c.execute("SELECT * FROM parts")
    items = c.fetchall()
    print(items)
    
#printing by column
def show_col(num):
    c.execute("SELECT * FROM parts")
    items = c.fetchall()
    for item in items:
        print(item[num])
        
#to show row ID (Primary key ID) when show all
def show_row_ID():
    c.execute("SELECT rowid,* FROM parts")
    items = c.fetchall()
    print(items)

#Using Where clause - enter comparison as equal, greater, or less than as well as the value and subject to compare 

def where_clause(subject, comparison, value):
    if comparison == 'equal':
        c.execute("SELECT * FROM parts WHERE {} = ?".format(subject), (value,))
    elif comparison == 'greater':
        c.execute("SELECT * FROM parts WHERE {} > ?".format(subject), (value,))
    elif comparison == 'less':
        c.execute("SELECT * FROM parts WHERE {} < ?".format(subject), (value,))
    elif comparison == 'less equal':
        c.execute("SELECT * FROM parts WHERE {} <= ?".format(subject), (value,))
    else:
        c.execute("SELECT * FROM parts WHERE {} >= ?".format(subject), (value,))

    items = c.fetchall()
    for item in items:
        print(item)  # printing row

# Update Records
def update_records(set_name, set_val, where, what):
    c.execute("""UPDATE parts SET {} = ? WHERE {} = ?""".format(set_name, where), (set_val, what))

#Query the Database - AND/OR
def query_andor(column1, operator1, value1, column2, operator2, value2, logical_operator):
    query = (f"SELECT rowid, * FROM parts WHERE {column1} {operator1} ? {logical_operator} {column2} {operator2} ?")
    if logical_operator == 'AND':
        c.execute(query, (value1, value2))
    elif logical_operator == 'OR':
        c.execute(query.replace('AND', 'OR'), (value1, value2))
    else:
        print("Invalid logical operator. Please use 'AND' or 'OR'.")

    results = c.fetchall()
    for row in results:
        print(row)

def delete_table():
    c.execute("DROP TABLE parts")
    
# Don't forget to close the connection when you're done
def close_connection():
    conn.close()


    

    





    
