from flask import Blueprint
from flask import render_template, Flask, request, url_for, redirect, session,jsonify
from forms import *
from features import *
from datetime import datetime, timedelta,date
import sqlite3

donatePage= Blueprint("donate", __name__)

@donatePage.route('/donate',methods=('GET','Post'))
def donate():
    searchForm=SearchForm()
    logoutForm=LogoutForm()
    donateForm=DonateForm()
    name=session.get('username')
    if donateForm.submit_button.data:
        conn=sqlite3.connect("library.db")
        conn.row_factory=sqlite3.Row
        query=donateItem()
        values=[donateForm.title.data,donateForm.description.data,donateForm.donateDate.data,donateForm.dropdown.data]
        conn.execute(query,values)
        conn.commit()
        conn.close()
        return render_template('blank.html',name=name,logoutForm=logoutForm,searchForm=searchForm,string="donating")
    if (logoutForm.logout_button.data):
        session['user_id']=None
        session['username']=None
    if (searchForm.search_button.data):
        search=request.form['search_bar']
        
        return redirect(url_for('Search.search',search=search))
    
    return render_template('donate.html',name=name,logoutForm=logoutForm, searchForm=searchForm, title='Donate', donateForm=donateForm)