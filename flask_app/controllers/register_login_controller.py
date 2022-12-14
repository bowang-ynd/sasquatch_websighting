from flask import render_template, request, redirect, flash, session
from flask_app import app, bcrypt

from flask_app.models.user_model import User


#? ==================== REGISTER and LOGIN ====================
#* render the login and register html page 
@app.route('/')
def register_and_login():
    if 'uid' in session:
        return redirect('/dashboard')
    return render_template('/register_login.html')

#* takes user's input of register info, checks if register info is valid
@app.route('/register', methods=['POST'])
def register():
    # checks if the user has inputed valid registration info
    if not User.validate_register(request.form):
        return redirect('/')

    # if user has valid registration info, register the user in the database
    data = {
        **request.form,
        'password' : bcrypt.generate_password_hash(request.form['password']),
    }

    User.register(data)
    session['uid'] = User.get_by_email(data).id
    return redirect('/dashboard')

#* takes user's input of login info, checks if login info is valid
@app.route('/login', methods=['POST'])
def login():
    # checks if the user has inputed valid login info
    data = {
        'email' : request.form['email'],
        'password' : request.form['password']
    }

    logged_in_user = User.validate_login(data)

    if not logged_in_user:
        return redirect('/')
    
    # if the user has valid login info, login the user and redirect the dashboard
    session['uid'] = logged_in_user.id

    return redirect('/dashboard')


#? ========== LOGOUT ==========
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


