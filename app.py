#import models
from models import Base, session, Book, engine
import datetime
import csv

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
    month = int(months.index(split_date[0]) + 1)
    day = int(split_date[1].split(',')[0])
    year = int(split_date[2])
    return datetime.date(year, month, day)
    # print(type(day))
    # datetime.date()

def clean_price(price_str):
    price_float = float(price_str)
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
            #add book
            pass
        elif choice == '2':
            pass
        elif choice == '3':
            pass
        elif choice == '4':
            pass
        elif choice == '5':
            print('Good-bye')
            app_running = False


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    #app()
    add_csv()
    for book in session.query(Book):
        print(book)