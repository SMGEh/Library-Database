from flask import Blueprint
from flask import render_template, Flask, request, url_for, redirect, session,jsonify
from forms import *
from features import *
from datetime import datetime, timedelta,date
import sqlite3

myItemsPage= Blueprint("myItems", __name__)

@myItemsPage.route('/myItems',methods=('GET','Post'))
def myItems():
    name = session.get('username')
    if(name == None):
        return redirect(url_for('login'))
    searchForm=SearchForm()
    logoutForm=LogoutForm()
    if (logoutForm.logout_button.data):
        session['user_id']=None
        session['username']=None
    if (searchForm.search_button.data):
        search=request.form['search_bar']
        
        return redirect(url_for('Search.search',search=search))
    name = session.get('username')
    conn=sqlite3.connect("library.db")
    conn.row_factory=sqlite3.Row
    query=userItems(session.get('user_id'))
    search_results=conn.execute(query).fetchall()
    conn.close()
    items=None
    return render_template('myItems.html',name=name,logoutForm=logoutForm, searchForm=searchForm, title='My items',  search_results=search_results)