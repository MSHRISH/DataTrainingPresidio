from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests


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
    print(username,password)
    # return {}
    url = "http://127.0.0.1:5000/login"
    data = {
        "username": username,
        "password": password
    }
    headers = {
        "Content-Type": "application/json",
    }

    # Use json parameter instead of data
    result = requests.post(url, json=data, headers=headers)
    print("test here")
    if result.status_code == 200:
        data = result.json()
        if data['result']==True:
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
    
    app.run(debug=True,port=8080)
