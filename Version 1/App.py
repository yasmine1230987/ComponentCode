
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Functions for interacting with the SQLite database

def connect_db():
    return sqlite3.connect('com.db')


# Query the Database - AND/OR
def query_andor_db(column1, operator1, value1, column2, operator2, value2, logical_operator):
    conn = connect_db()
    c = conn.cursor()
    query = f"SELECT rowid, * FROM parts WHERE {column1} {operator1} ? {logical_operator} {column2} {operator2} ?"
    if logical_operator == 'AND':
        c.execute(query, (value1, value2))
    elif logical_operator == 'OR':
        c.execute(query.replace('AND', 'OR'), (value1, value2))
    else:
        raise ValueError("Invalid logical operator. Please use 'AND' or 'OR'.")
    results = c.fetchall()
    conn.close()
    return results

def create_table():
    conn = connect_db()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS parts (
        Material REAL,
        Batch REAL,
        CodeA REAL,
        CodeB REAL,
        CodeC REAL,
        CodeD REAL
    )""")
    conn.commit()
    conn.close()

def insert_row(materialID, BatchID, CodeA, CodeB, CodeC, CodeD):
    conn = connect_db()
    c = conn.cursor()
    c.execute("INSERT INTO parts VALUES (?, ?, ?, ?, ?, ?)", (materialID, BatchID, CodeA, CodeB, CodeC, CodeD))
    conn.commit()
    conn.close()

# Query all data
def query_all_data():
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM parts")
    items = c.fetchall()
    conn.close()
    return items

def insert_many(all_parts):
    conn = connect_db()
    c = conn.cursor()
    c.executemany("INSERT INTO parts VALUES (?, ?, ?, ?, ?, ?)", all_parts)
    conn.commit()
    conn.close()

#Where clause
def where_clause_db(subject, comparison, value):
    conn = connect_db()
    c = conn.cursor()
    if comparison == 'equal':
        c.execute("SELECT * FROM parts WHERE {} = ?".format(subject), (value,))
    elif comparison == 'greater':
        c.execute("SELECT * FROM parts WHERE {} > ?".format(subject), (value,))
    elif comparison == 'less':
        c.execute("SELECT * FROM parts WHERE {} < ?".format(subject), (value,))
    elif comparison == 'less equal':
        c.execute("SELECT * FROM parts WHERE {} <= ?".format(subject), (value,))
    elif comparison =='greater equal':
        c.execute("SELECT * FROM parts WHERE {} >= ?".format(subject), (value,))
    else:
         raise ValueError("Invalid operator. Please use 'equal' 'greater' 'less' 'less equal' 'greater equal'.")

    results = c.fetchall()
    conn.close()
    return results

# Update Records
def update_records_db(set_name, set_val, where, what):
    conn = connect_db()
    c = conn.cursor()
    c.execute("""UPDATE parts SET {} = ? WHERE {} =  ?""".format(set_name, where), (set_val, what))
    conn.commit()
    conn.close()


#Remove Parts
def remove_part_db(to_change, materialID, batchID, new_value):
    conn = connect_db()
    c = conn.cursor()
    # Fetch the current value from the database
    c.execute('''SELECT {} FROM parts WHERE Material = ? and Batch = ?'''.format(to_change), (materialID, batchID))
    current_value = c.fetchone()[0]
    # Calculate the new value
    new_value=float(new_value)
    updated_value = current_value - new_value
    # Update the value in the specified cell
    c.execute('''UPDATE parts SET {} = ? WHERE Material = ? AND Batch = ?'''.format(to_change), (updated_value, materialID, batchID))
    conn.commit()
    conn.close()


# Define routes for web application

@app.route('/')

def index():
    return render_template('index.html')

@app.route('/add_part', methods=['GET', 'POST'])
def add_part():
    if request.method == 'POST':
        materialID = request.form['materialID']
        BatchID = request.form['BatchID']
        CodeA = request.form['CodeA']
        CodeB = request.form['CodeB']
        CodeC = request.form['CodeC']
        CodeD = request.form['CodeD']
        insert_row(materialID, BatchID, CodeA, CodeB, CodeC, CodeD)
        return redirect(url_for('index'))
    return render_template('add_part.html')

@app.route('/show_table', methods=['GET','POST'])
def show_table():
    if request.method == 'POST':
        # Handle any POST request logic here, if needed
        pass
    
    # Query all data from the database
    data = query_all_data()
    
    # Render the show_all.html template with the fetched data
    return render_template('show_table.html', data=data)

@app.route('/query_andor', methods=['GET', 'POST'])
def query_andor():
    if request.method == 'POST':
        # Get form data
        column1 = request.form['column1']
        operator1 = request.form['operator1']
        value1 = request.form['value1']
        column2 = request.form['column2']
        operator2 = request.form['operator2']
        value2 = request.form['value2']
        logical_operator = request.form['logical_operator']

        # Call the query_andor function
        results = query_andor_db(column1, operator1, value1, column2, operator2, value2, logical_operator)

        # Render the results template
        return render_template('results.html', results=results)

    # If request method is not POST, render the form template
    return render_template('query_andor.html')

@app.route('/where_clause', methods=['GET', 'POST'])
def where_clause():
    if request.method == 'POST':
        subject = request.form['subject']
        comparison = request.form['comparison']
        value = request.form['value']
        # call the where_clause function

        results = where_clause_db(subject,comparison,value)

        #Render the results template
        return render_template('results.html', results=results)
    return render_template('where_clause.html')
    
@app.route('/update_records', methods=['GET', 'POST'] )
def update_records():
    if request.method == 'POST':
        set_name=request.form['subject']
        set_val=request.form['set_val']
        where=request.form['where']
        what=request.form['what']

        #call update_records function

        update_records_db(set_name,set_val,where,what)
        #maybe add a accomplished message

    return render_template('update_records.html')
@app.route('/remove_part', methods = ['GET', 'POST'] )
def remove_part():
    if request.method=='POST':
        to_change=request.form['to_change']
        materialID = request.form['materialID']
        batchID = request.form['batchID']
        new_value = request.form['new_value']

        #call remove_part function
        remove_part_db(to_change,materialID,batchID,new_value)
    return render_template('remove_part.html')


if __name__ == '__main__':
    create_table()
    app.run(host="0.0.0.0", 
    port=5000,
    debug=True,
    threaded=True)
