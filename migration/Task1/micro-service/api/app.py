from flask import Flask, render_template, request, redirect, url_for, flash, session
import pyodbc
import os
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Azure SQL Server connection setup
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=tcp:testserver6.database.windows.net;'
    'DATABASE=migrationtest;'
    'UID=shrish;'
    'PWD=Pa$$word;'
    'Encrypt=yes;'
    'TrustServerCertificate=no;'
    'Connection Timeout=30;'
)

@app.route('/login', methods=['POST'])
def login_check():
    data = request.get_json()
    print("test")
    print(data['username'])
    username = data['username']
    password = data['password']
    
    
    
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(1) FROM AuthTable WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()

    if result[0]:
        return {"result":True}
    else:
        return {"result":False}


if __name__ == '__main__':
    app.run(debug=True)
