from flask import Flask, render_template, request, redirect, url_for, flash, session
import pyodbc
import os
import sqlite3

DATABASE = 'users.db'

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/home')
def welcome():
    if 'logged_in' in session:
        return render_template('home.html', username=session['username'])
    else:
        flash('Please log in first!')
        return redirect(url_for('home'))



@app.route('/login', methods=['POST'])
def login_check():
    username = request.form['username']
    password = request.form['password']
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(1) FROM users WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()

    if result[0]:
        session['logged_in'] = True
        session['username'] = username
        return redirect(url_for('welcome'))
    else:
        flash('Invalid username or password!')
        return redirect(url_for('home'))
 
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('You have been logged out!')
    return redirect(url_for('home'))

if __name__ == '__main__':
    
    app.run(debug=True)
