import sqlite3
from flask import render_template, Flask, request, url_for, redirect, session, Blueprint
from forms import *
from datetime import datetime, timedelta,date
from features import *
from pages.askUsPage.routes import askUsPage
from pages.checkoutPage.routes import checkOutPage
from pages.donatePage.routes import donatePage
from pages.eventRegPage.routes import eventsRegPage
from pages.eventsPage.routes import eventsPage
from pages.loginPage.routes import loginPage
from pages.myEventsPage.routes import myEventsPage
from pages.myItemsPage.routes import myItemsPage
from pages.searchPage.routes import searchPage
from pages.volunteerPage.routes import volunteerPage


app = Flask(__name__)
app.config['SECRET_KEY']='CMPT354'

app.register_blueprint(askUsPage)
app.register_blueprint(checkOutPage)
app.register_blueprint(donatePage)
app.register_blueprint(eventsRegPage)
app.register_blueprint(eventsPage)
app.register_blueprint(loginPage)
app.register_blueprint(myEventsPage)
app.register_blueprint(myItemsPage)
app.register_blueprint(searchPage)
app.register_blueprint(volunteerPage)


@app.route('/', methods=('GET', 'POST'))

@app.route('/index', methods=('GET', 'POST'))
def index():

    searchForm=SearchForm()
    logoutForm=LogoutForm()
    name=session.get('username')
    if (logoutForm.logout_button.data):
        session['user_id']=None
        session['username']=None
        return redirect(url_for('index'))
    if (searchForm.search_button.data):
        search=request.form['search_bar']        
        return redirect(url_for('Search.search',search=search))
    return render_template('top.html',name=name,logoutForm=logoutForm,searchForm=searchForm)