from flask import Blueprint
from flask import render_template, Flask, request, url_for, redirect, session,jsonify
from forms import *
from features import *
from datetime import datetime, timedelta,date
import sqlite3

loginPage= Blueprint("login", __name__)

@loginPage.route('/login',methods=('GET','POST'))
def login(invalid=None):
    
    searchForm=SearchForm()
    logoutForm=LogoutForm()
    name=session.get('username')
    
    if(name!=None):
        return redirect(url_for('index'))
    
    loginForm=LoginForm()
    if (logoutForm.logout_button.data):
        session['user_id']=None
        session['username']=None

    if (searchForm.search_button.data):
        search=request.form['search_bar']
        
        return redirect(url_for('Search.search',search=search))
    
    if (loginForm.submit.data):
        num=loginForm.number.data
        password=loginForm.password.data
        conn=conn=sqlite3.connect("library.db")
        conn.row_factory=sqlite3.Row
        real_password=conn.execute(f'SELECT pwd FROM Users WHERE UserID={num}').fetchone()
        conn.close()
        if(password==real_password['pwd']):
            session['user_id'] = num
            session['username']= 'steve' #conn.execute(f'SELECT User_fname FROM Users WHERE UserID={num}').fetchall()
            
            return redirect(url_for('index'))
        '''else:
            conn.close()
            return redirect(url_for('index',invalid=True))'''

    
    return render_template('login.html',name=name,logoutForm=logoutForm, title='Log In', searchForm=searchForm, loginForm=loginForm,incorrect=invalid)
