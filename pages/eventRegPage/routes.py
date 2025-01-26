from flask import Blueprint
from flask import render_template, Flask, request, url_for, redirect, session,jsonify
from forms import *
from features import *
from datetime import datetime, timedelta,date
import sqlite3

eventsRegPage= Blueprint("eventRegister", __name__)

@eventsRegPage.route('/eventRegister<int:eventID>',methods=('GET','Post'))
def eventRegister(eventID):
    searchForm=SearchForm()
    logoutForm=LogoutForm()
    submit=Register()
    name=session.get('username')
    if(submit.unregister_button.data):
        conn=sqlite3.connect("library.db")
        conn.row_factory=sqlite3.Row
        query="DELETE FROM EVENTREGISTRATION WHERE eventID = ? AND userID = ?"
        data=[eventID,session.get('user_id')]
        conn.execute(query,data)
        conn.commit()
        conn.close()
    if(submit.submit_button.data):
        conn=sqlite3.connect("library.db")
        conn.row_factory=sqlite3.Row
        query="INSERT INTO EVENTREGISTRATION('EventID', 'UserID', 'ERegistration_date') VALUES (?,?,?)"
        data=[eventID,session.get('user_id'),datetime.now().date()]
        conn.execute(query,data)
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
    query=eventQuery(eventID)
    event=conn.execute(query).fetchone()
    query=query=f'''SELECT * FROM EVENTREGISTRATION 
    left join events on eventregistration.eventID=events.eventid
    where USERid={session['user_id']} and eventregistration.eventID={eventID}'''
    registeredEvents=conn.execute(query).fetchall()
    conn.close()
    return render_template('event.html',name=name,logoutForm=logoutForm, searchForm=searchForm, title=eventID, event=event, submit=submit,registered=(len(registeredEvents))>0)