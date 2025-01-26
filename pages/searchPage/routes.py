from flask import Blueprint
from flask import render_template, Flask, request, url_for, redirect, session,jsonify
from forms import *
from features import *
from datetime import datetime, timedelta,date
import sqlite3
import sys

searchPage= Blueprint("Search", __name__)

@searchPage.route('/search/<string:search>',methods=('GET','Post'))
def search(search):
    print("heere"+search, file=sys.stderr)
    searchForm = SearchForm()
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
    
    
    query=searchDatatbase(search)
    
    search_results=conn.execute(query).fetchall()
    conn.close()
    return render_template('search.html',name=name,logoutForm=logoutForm, title=search, searchForm=searchForm,search=search,search_results=search_results)

@searchPage.route('/search/',methods=('GET','Post'))
def empty_search():
    searchForm = SearchForm()
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
    
    search=""
    
    query=searchDatatbase(search)
    
    search_results=conn.execute(query).fetchall()
    conn.close()
    return render_template('search.html',name=name,logoutForm=logoutForm, title=search, searchForm=searchForm,search=search,search_results=search_results)