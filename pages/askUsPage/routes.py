from flask import Blueprint
from flask import render_template, Flask, request, url_for, redirect, session,jsonify
from forms import *

askUsPage= Blueprint("askUs", __name__)

@askUsPage.route('/askUs',methods=('GET','Post'))
def askUs():
    searchForm=SearchForm()
    logoutForm=LogoutForm()
    name=session.get('username')
    if (logoutForm.logout_button.data):
        session['user_id']=None
        session['username']=None
    if (searchForm.search_button.data):
        search=request.form['search_bar']
        
        return redirect(url_for('Search.search',search=search))
    return render_template('askUs.html',name=name,logoutForm=logoutForm, searchForm=searchForm, title='Ask Us')