from flask import Blueprint
from flask import render_template, Flask, request, url_for, redirect, session,jsonify
from forms import *
from features import *
from datetime import datetime, timedelta,date
import sqlite3

checkOutPage= Blueprint("itemCheckOut", __name__)

@checkOutPage.route('/itemCheckOut/<int:item>',methods=('GET','Post'))
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
        return redirect(url_for('Search.search',search=search))
    
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