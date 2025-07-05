#import models
from models import Base, session, Book, engine
import datetime
import csv
import time

#main menu
def menu():
    while True:
        print('''
                Programming Books
                \r1) Add Book
                \r2) View All Books
                \r3) Search Books
                \r4) Book Analysis
                \r5) Exit''')
        choice = input('What would you like to do?\n')
        if choice in ['1','2','3','4','5']:
            return choice
        else:
            print('Please choose one of the options below.\n'
            'A number from 1 - 5.')
def clean_date(date_str):
    months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"]
    split_date = date_str.split(' ')
    try:
        month = int(months.index(split_date[0]) + 1)
        day = int(split_date[1].split(',')[0])
        year = int(split_date[2])
        return_date = datetime.date(year, month, day)
    except ValueError:
        input('''
\n*****Date Error*****
              \rThe date format should include a valid Month Day ,and then year
              \rPlease Try again.
              \rEx: February 13, 1992''')
        return
    else: 
        return return_date

def clean_price(price_str):
    try:
        price_float = float(price_str)
    except ValueError:
        input('''
\n*****Price Error*****
              \rThe price format should include a valid Price without a currency symbol
              \rPlease Try again.
              \rEx: 21.99''')
    else:
        return int(price_float * 100)



    
    return int(price_float * 100)



def add_csv():
    with open('suggested_books.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            book_in_db = session.query(Book).filter(Book.title == row[0]).one_or_none()
            if book_in_db == None:
                title = row[0]
                author = row[1]
                date = clean_date(row[2])
                price = clean_price(row[3])
                new_book = Book(title=title, author=author, published_date = date, price=price)
                session.add(new_book)
        session.commit()



def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == '1':
            title = input('Title: ')
            author = input('Author: ')
            date_error = True
            while date_error:
                date = input('Date (EX: July 16, 2013): ')
                date = clean_date(date)
                if type(date) == datetime.date:
                    date_error = False
            price_error = True
            while price_error:
                price = input('Price (Ex:25.04)')
                price = clean_price(price)
                if type(price) == int:
                    price_error = False
            new_book = Book(title=title, author=author, published_date=date, price=price)
            session.add(new_book)
            session.commit()
            print('Book Added Successfully')
            time.sleep(1.5)
        elif choice == '2':
            for book in session.query(Book):
                print(f'{book.id} | {book.title} | {book.author} | {book.price}')
            input('\nPress enter to return to the main menu.')
        elif choice == '3':
            pass
        elif choice == '4':
            pass
        elif choice == '5':
            print('Good-bye')
            app_running = False


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app()
    # add_csv()
    for book in session.query(Book):
        print(book)