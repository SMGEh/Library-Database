from flask import Blueprint
from flask import render_template, Flask, request, url_for, redirect, session,jsonify
from forms import *
from features import *
from datetime import datetime, timedelta,date
import sqlite3

eventsPage= Blueprint("events", __name__)

@eventsPage.route('/events',methods=('GET','Post'))
def events():
    searchForm=SearchForm()
    logoutForm=LogoutForm()
    name = session.get('username')
    if (logoutForm.logout_button.data):
        session['user_id']=None
        session['username']=None
    if (searchForm.search_button.data):
        search=request.form['search_bar']
        
        return redirect(url_for('Search.search',search=search))
    
    conn=sqlite3.connect("library.db")
    conn.row_factory=sqlite3.Row
    query=eventListQuery()
    eventsList=conn.execute(query).fetchall()
    conn.close()

    return render_template('eventList.html',name=name,logoutForm=logoutForm, searchForm=searchForm, title='Events', eventsList=eventsList)