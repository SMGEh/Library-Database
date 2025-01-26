
def searchDatatbase(search):
    if search=="":
        query=f'''SELECT * FROM Item 
    left join book ON book.item_id=item.item_id
    left join magazine ON magazine.item_id=item.item_id
    left join cd ON cd.item_id=item.item_id
    left join record ON record.item_id=item.item_id
    left join journal ON journal.item_id=item.item_id
    left join movie ON movie.item_id=item.item_id
    '''
        

    else:
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