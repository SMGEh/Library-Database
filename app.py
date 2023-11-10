import sqlite3
from flask import render_template, Flask, request, url_for, redirect, session,jsonify
from forms import *
from datetime import datetime, timedelta,date   


app = Flask(__name__)
app.config['SECRET_KEY']='CMPT354'




def searchDatatbase(search):
    query=f'''SELECT * FROM Item 
    left join book ON book.item_id=item.item_id
    left join magazine ON magazine.item_id=item.item_id
    left join cd ON cd.item_id=item.item_id
    left join record ON record.item_id=item.item_id
    left join journal ON journal.item_id=item.item_id
    left join movie ON movie.item_id=item.item_id
    where
    book.book_title like '%{search}%' or
    book.book_author like '%{search}%' or
    magazine.magazine_title like '%{search}%' or
    magazine.magazine_publisher like '%{search}%' or
    cd.cd_title like '%{search}%' or
    cd.cd_artist like '%{search}%' or
    cd.cd_publisher like '%{search}%' or
    record.record_title like '%{search}%' or
    record.record_artist like '%{search}%' or
    record.record_publisher like '%{search}%' or
    journal.journal_title like '%{search}%' or
    journal.journal_publisher like '%{search}%' or
    movie.movie_title like '%{search}%' or 
    movie.movie_director like '%{search}%' or
    movie.movie_cast like '%{search}%' '''
    return query

def itemData(item_id):
    query=f'''SELECT * FROM Item 
    left join book ON book.item_id=item.item_id
    left join magazine ON magazine.item_id=item.item_id
    left join cd ON cd.item_id=item.item_id
    left join record ON record.item_id=item.item_id
    left join journal ON journal.item_id=item.item_id
    left join movie ON movie.item_id=item.item_id
    left join ItemAvailability ON ItemAvailability.Availability_ID=item.item_id
    where
    item.item_id={item_id} '''
    return query

def checkOutItem():
    query=f'''INSERT INTO Borrowing_History('UserID', 'Item_id', 'issue_date', 'Return_date') VALUES (?, ?, ?, ?)'''
    return query

def checkItemCheckout(item_id,userID):
    query=f'''SELECT * FROM Item
            left join borrowing_history ON borrowing_history.item_id=item.item_id
            where
            item.item_id={item_id} and
            borrowing_history.userID={userID}'''
    return query

def loginQuery(number,password):
    query=f'''SELECT * FROM Users
            where
            UserID={number} and
            password={password}'''
    return query

def userItems(userID):
    query=f'''SELECT * FROM borrowing_history
    left join item ON item.item_id=borrowing_history.item_id 
    left join book ON book.item_id=borrowing_history.item_id
    left join magazine ON magazine.item_id=borrowing_history.item_id
    left join cd ON cd.item_id=borrowing_history.item_id
    left join record ON record.item_id=borrowing_history.item_id
    left join journal ON journal.item_id=borrowing_history.item_id
    left join movie ON movie.item_id=borrowing_history.item_id
    left join fines ON fines.borrowingID=borrowing_history.borrowingID
    where
    UserID={userID}'''
    return query

def donateItem():
    query=f'''INSERT INTO Future_additions('Future_Item_name', 'Future_item_description', 'Exp_date', 'Future_item_type') VALUES(?, ?, ?, ?)'''
    return query

def eventListQuery():
    query=f'''SELECT * FROM EVENTS'''
    return query

def eventQuery(event_id):
    query=f'''SELECT * FROM EVENTS where eventID={event_id}'''
    return query

def volunteerQuery():
    query=f'''INSERT INTO Volunteers('UserID', 'Vol_availability', 'Vol_experience', 'Vol_interests', 'Vol_earliest_start', 'Vol_end_date') VALUES(?, ?, ?, ?, ?, ?)'''
    return query

def myEventsQuery(userID):
    query=f'''SELECT * FROM EVENTREGISTRATION 
    left join events on eventregistration.eventID=events.eventid
    where USERid={userID}'''
    return query

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
        
        return redirect(url_for('search',search=search))
    return render_template('top.html',name=name,logoutForm=logoutForm,searchForm=searchForm)

@app.route('/login',methods=('GET','POST'))
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
        
        return redirect(url_for('search',search=search))
    
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

@app.route('/search/<string:search>',methods=('GET','Post'))
def search(search):
    searchForm = SearchForm()
    logoutForm=LogoutForm()
    if (logoutForm.logout_button.data):
        session['user_id']=None
        session['username']=None
    if (searchForm.search_button.data):
        search=request.form['search_bar']
        
        return redirect(url_for('search',search=search))
    name = session.get('username')
    conn=sqlite3.connect("library.db")
    conn.row_factory=sqlite3.Row
    query=searchDatatbase(search)
    search_results=conn.execute(query).fetchall()
    conn.close()
    return render_template('search.html',name=name,logoutForm=logoutForm, title=search, searchForm=searchForm,search=search,search_results=search_results)

@app.route('/itemCheckOut/<int:item>',methods=('GET','Post'))
def itemCheckOut(item):
    searchForm=SearchForm()
    logoutForm=LogoutForm()
    checkoutForm=CheckoutForm()
    name=session.get('username')
    if(checkoutForm.returnItem.data):
        if(name == None):
            return redirect(url_for('login'))
        conn=sqlite3.connect("library.db")
        conn.row_factory=sqlite3.Row
        query=checkItemCheckout(item,session.get('user_id'))
        checkedOut=conn.execute(query).fetchone()
        query="DELETE FROM Borrowing_History WHERE borrowingID = ?"
        data=[checkedOut['BorrowingID']]
        conn.execute(query,data)
        query=f"SELECT * FROM ITEMAVAILABILITY WHERE AVAILABILITY_ID={item}"
        available=conn.execute(query).fetchone()
        query=F"UPDATE ItemAvailability SET available_copies = ? WHERE AVAILABILITY_ID={item}"
        if(int(available['available_copies'])<int(available['item_totalNo'])):
            data=[available['available_copies']+1]
            conn.execute(query,data)
        
        conn.commit()
        conn.close()

    elif(checkoutForm.renew.data):
        if(name == None):
            return redirect(url_for('login'))
        conn=sqlite3.connect("library.db")
        conn.row_factory=sqlite3.Row
        
        today=datetime.now().date()
        retDate=today+timedelta(weeks=2)
        query=checkItemCheckout(item,session.get('user_id'))
        checkedOut=conn.execute(query).fetchone()
        query=f"select * from renewals where borrowingID={checkedOut['BorrowingID']}"
        checkedOut=len(conn.execute(query).fetchall())
        if(len==0):
            query="INSERT INTO Renewals('BorrowingID', 'Renewal_status', 'Renewal_date', 'Renewal_reason') VALUES (?,?,?,?)"
            data=[checkedOut['BorrowingID'],'Pending',today,checkoutForm.renewReason.data]
            conn.execute(query,data)
            print('done')
        conn.commit()
        conn.close()
        print("no renew")
        


    elif(checkoutForm.submit_button.data):
        conn=sqlite3.connect("library.db")
        conn.row_factory=sqlite3.Row
        query=checkOutItem()
        today=datetime.now().date()
        retDate=today+timedelta(weeks=2)
        data=[session.get('user_id'),item,today,retDate]
        conn.execute(query,data)
        query=f"SELECT * FROM ITEMAVAILABILITY WHERE AVAILABILITY_ID={item}"
        available=conn.execute(query).fetchone()
        query=F"UPDATE ItemAvailability SET available_copies = ? WHERE AVAILABILITY_ID={item}"
        data=[int(available['available_copies'])-1]
        conn.execute(query,data)
        conn.commit()
        conn.close()

    
    if (logoutForm.logout_button.data):
        session['user_id']=None
        session['username']=None

    if (searchForm.search_button.data):
        search=request.form['search_bar']
        return redirect(url_for('search',search=search))
    
    checkedOut=0
    conn=sqlite3.connect("library.db")
    conn.row_factory=sqlite3.Row
    query=itemData(item)
    search_results=conn.execute(query).fetchone()
    if(session.get('user_id')!=None):
        query=checkItemCheckout(item,session.get('user_id'))
        checkedOut=len(conn.execute(query).fetchall())
    conn.close()
    
    return render_template('item.html',name=name,logoutForm=logoutForm, searchForm=searchForm, search_result=search_results, checkoutForm=checkoutForm, checkedOut=checkedOut)

@app.route('/myItems',methods=('GET','Post'))
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
        
        return redirect(url_for('search',search=search))
    name = session.get('username')
    conn=sqlite3.connect("library.db")
    conn.row_factory=sqlite3.Row
    query=userItems(session.get('user_id'))
    search_results=conn.execute(query).fetchall()
    conn.close()
    items=None
    return render_template('myItems.html',name=name,logoutForm=logoutForm, searchForm=searchForm, title='My items',  search_results=search_results)

@app.route('/volunteer',methods=('GET','Post'))
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
        
        return redirect(url_for('search',search=search))
    
    conn=sqlite3.connect("library.db")
    conn.row_factory=sqlite3.Row
    query=f'''SELECT * FROM VOLUNTEERs WHERE userid={session.get('user_id')}'''
    results=len(conn.execute(query).fetchall())
    conn.close()
    return render_template('volunteer.html',name=name,logoutForm=logoutForm, searchForm=searchForm, title='Volunteer',volunteer=volunteer,inTable=results)

@app.route('/donate',methods=('GET','Post'))
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
        
        return redirect(url_for('search',search=search))
    
    return render_template('donate.html',name=name,logoutForm=logoutForm, searchForm=searchForm, title='Donate', donateForm=donateForm)

@app.route('/events',methods=('GET','Post'))
def events():
    searchForm=SearchForm()
    logoutForm=LogoutForm()
    name = session.get('username')
    if (logoutForm.logout_button.data):
        session['user_id']=None
        session['username']=None
    if (searchForm.search_button.data):
        search=request.form['search_bar']
        
        return redirect(url_for('search',search=search))
    
    conn=sqlite3.connect("library.db")
    conn.row_factory=sqlite3.Row
    query=eventListQuery()
    eventsList=conn.execute(query).fetchall()
    conn.close()
    return render_template('eventlist.html',name=name,logoutForm=logoutForm, searchForm=searchForm, title='Events', eventsList=eventsList)

@app.route('/eventRegister<int:eventID>',methods=('GET','Post'))
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
        
        return redirect(url_for('search',search=search))
    
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

@app.route('/myEvents',methods=('GET','Post'))
def myEvents():
    searchForm=SearchForm()
    logoutForm=LogoutForm()
    name=session.get('username')
    if (logoutForm.logout_button.data):
        session['user_id']=None
        session['username']=None
    if (searchForm.search_button.data):
        search=request.form['search_bar']
        
        return redirect(url_for('search',search=search))
    if(name==None):
        return redirect(url_for('login'))
    conn=sqlite3.connect("library.db")
    conn.row_factory=sqlite3.Row
    query=myEventsQuery(session['user_id'])
    events=conn.execute(query).fetchall()
    conn.close()
    return render_template('myEvents.html',name=name,logoutForm=logoutForm, events=events, searchForm=searchForm, title='My Events')

@app.route('/askUs',methods=('GET','Post'))
def askUs():
    searchForm=SearchForm()
    logoutForm=LogoutForm()
    name=session.get('username')
    if (logoutForm.logout_button.data):
        session['user_id']=None
        session['username']=None
    if (searchForm.search_button.data):
        search=request.form['search_bar']
        
        return redirect(url_for('search',search=search))
    return render_template('askUs.html',name=name,logoutForm=logoutForm, searchForm=searchForm, title='Ask Us')
