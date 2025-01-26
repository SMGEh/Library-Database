from flask import Blueprint
from flask import render_template, Flask, request, url_for, redirect, session,jsonify
from forms import *
from features import *
from datetime import datetime, timedelta,date
import sqlite3

myEventsPage= Blueprint("myEvents", __name__)

@myEventsPage.route('/myEvents',methods=('GET','Post'))
def myEvents():
    searchForm=SearchForm()
    logoutForm=LogoutForm()
    name=session.get('username')
    if (logoutForm.logout_button.data):
        session['user_id']=None
        session['username']=None
    if (searchForm.search_button.data):
        search=request.form['search_bar']
        
        return redirect(url_for('Search.search',search=search))
    if(name==None):
        return redirect(url_for('login'))
    conn=sqlite3.connect("library.db")
    conn.row_factory=sqlite3.Row
    query=myEventsQuery(session['user_id'])
    events=conn.execute(query).fetchall()
    conn.close()
    return render_template('myEvents.html',name=name,logoutForm=logoutForm, events=events, searchForm=searchForm, title='My Events')