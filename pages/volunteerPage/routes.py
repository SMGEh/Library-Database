from flask import Blueprint
from flask import render_template, Flask, request, url_for, redirect, session,jsonify
from forms import *
from features import *
from datetime import datetime, timedelta,date
import sqlite3

volunteerPage= Blueprint("volunteer", __name__)


@volunteerPage.route('/volunteer',methods=('GET','Post'))
def volunteer():
    searchForm=SearchForm()
    logoutForm=LogoutForm()
    volunteer=Volunteer()
    name=session.get('username')

    if(volunteer.submit_button.data):
        conn=sqlite3.connect("library.db")
        conn.row_factory=sqlite3.Row
        query=volunteerQuery()
        values=[session['user_id'],volunteer.availability.data,volunteer.experience.data,volunteer.interests.data,volunteer.startDate.data,volunteer.endDate.data]
        conn.execute(query,values)
        conn.commit()
        conn.close()
        return render_template('blank.html',name=name,logoutForm=logoutForm,searchForm=searchForm,string="volunteering")
    if(volunteer.unregister_button.data):
        conn=sqlite3.connect("library.db")
        conn.row_factory=sqlite3.Row
        query="DELETE FROM VOLUNTEERS WHERE userID = ?"
        values=[session['user_id']]
        conn.execute(query,values)
        conn.commit()
        conn.close()
    if (logoutForm.logout_button.data):
        session['user_id']=None
        session['username']=None
    if (searchForm.search_button.data):
        search=request.form['search_bar']
        
        return redirect(url_for('Search.search',search=search))
    
    conn=sqlite3.connect("library.db")
    conn.row_factory=sqlite3.Row
    query=f'''SELECT * FROM VOLUNTEERs WHERE userid={session.get('user_id')}'''
    results=len(conn.execute(query).fetchall())
    conn.close()
    return render_template('volunteer.html',name=name,logoutForm=logoutForm, searchForm=searchForm, title='Volunteer',volunteer=volunteer,inTable=results)
