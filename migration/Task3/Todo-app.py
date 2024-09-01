from flask import Flask, request, jsonify
import pyodbc
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Azure SQL Server connection setup
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=tcp:shrish.database.windows.net;'
    'DATABASE=todolistapp;'
    'UID=shrish;'   
    'PWD=Pa$$word;'
    'Encrypt=yes;'
    'TrustServerCertificate=no;'
    'Connection Timeout=30;'
)

@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    first_name = data.get('firstname')
    last_name = data.get('lastname')
    username = data.get('username')
    password = data.get('password')

    cursor = conn.cursor()

    # Check if the username already exists
    cursor.execute("SELECT COUNT(1) FROM Users WHERE username = ?", (username,))
    result = cursor.fetchone()

    if result[0]:
        return {"result": False, "message": "Username already exists"}, 400

    # Insert the new user into the AuthTable
    cursor.execute(
        "INSERT INTO Users (firstname, lastname, username, password) VALUES (?, ?, ?, ?)",
        (first_name, last_name, username, password)
    )
    conn.commit()

    return {"result": True, "message": "User registered successfully"}, 201


@app.route('/login', methods=['POST'])
def login_check():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(1) FROM Users WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()

    if result[0]:
        return {"result": True}
    else:
        return {"result": False}



@app.route('/add-todo', methods=['POST'])
def add_todo():
    data = request.get_json()
    title = data.get('title')
    user_id = data.get('userid')
    description = data.get('description')
    target_date = data.get('targetdate')
    

    # Ensure target_date is in the correct format
    try:
        target_date = datetime.strptime(target_date, '%Y-%m-%d')
    except ValueError:
        return {"result": False, "message": "Invalid date format. Use YYYY-MM-DD."}, 400

    cursor = conn.cursor()

    # Insert the new todo item into the Todo table
    cursor.execute(
        "INSERT INTO Todo (title, userid, description, targetdate, status) VALUES (?, ?, ?, ?, ?)",
        (title, user_id, description, target_date, 0)
    )
    conn.commit()

    return {"result": True, "message": "Todo item added successfully"}, 201

@app.route('/delete-todo/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    cursor = conn.cursor()

    # Check if the todo item exists
    cursor.execute("SELECT COUNT(1) FROM Todo WHERE id = ?", (todo_id,))
    result = cursor.fetchone()

    if result[0] == 0:
        return {"result": False, "message": "Todo item not found"}, 404

    # Delete the todo item from the Todo table
    cursor.execute("DELETE FROM Todo WHERE id = ?", (todo_id,))
    conn.commit()

    return {"result": True, "message": "Todo item deleted successfully"}, 200

@app.route('/update-todo/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    target_date = data.get('targetdate')
    status = data.get('status')

    cursor = conn.cursor()

    # Check if the todo item exists
    cursor.execute("SELECT COUNT(1) FROM Todo WHERE id = ?", (todo_id,))
    result = cursor.fetchone()

    if result[0] == 0:
        return {"result": False, "message": "Todo item not found"}, 404

    # Prepare update query with only the fields that are provided
    update_query = "UPDATE Todo SET "
    update_params = []

    if title is not None:
        update_query += "title = ?, "
        update_params.append(title)
    
    if description is not None:
        update_query += "description = ?, "
        update_params.append(description)
    
    if target_date is not None:
        try:
            target_date = datetime.strptime(target_date, '%Y-%m-%d')
            update_query += "targetdate = ?, "
            update_params.append(target_date)
        except ValueError:
            return {"result": False, "message": "Invalid date format. Use YYYY-MM-DD."}, 400

    if status is not None:
        update_query += "status = ? "
        update_params.append(status)
    
    update_query += "WHERE id = ?"
    update_params.append(todo_id)

    cursor.execute(update_query, tuple(update_params))
    conn.commit()

    return {"result": True, "message": "Todo item updated successfully"}, 200


@app.route('/view-todo/<int:todo_id>', methods=['GET'])
def view_todo(todo_id):
    cursor = conn.cursor()

    # Retrieve the todo item by id
    cursor.execute("SELECT * FROM Todo WHERE id = ?", (todo_id,))
    todo = cursor.fetchone()

    if todo is None:
        return {"result": False, "message": "Todo item not found"}, 404

    todo_item = {
        "id": todo[0],
        "title": todo[1],
        "user_id": todo[2],
        "description": todo[3],
        "target_date": todo[4].strftime('%Y-%m-%d') if todo[4] else None,
        "status": todo[5]
    }

    return {"result": True, "todo": todo_item}, 200

@app.route('/todos/<int:user_id>', methods=['GET'])
def get_user_todos(user_id):
    cursor = conn.cursor()

    # Retrieve all todo items for the user
    cursor.execute("SELECT * FROM Todo WHERE userid = ?", (user_id,))
    todos = cursor.fetchall()

    if not todos:
        return {"result": False, "message": "No todo items found for this user"}, 404

    todo_list = []
    for todo in todos:
        todo_item = {
            "id": todo[0],
            "title": todo[1],
            "userid": todo[2],
            "description": todo[3],
            "targetdate": todo[4].strftime('%Y-%m-%d') if todo[4] else None,
            "status": todo[5]
        }
        todo_list.append(todo_item)

    return {"result": True, "todos": todo_list}, 200


if __name__ == '__main__':
    app.run(debug=True)
