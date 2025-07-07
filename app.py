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

def submenu():
    while True:
        print('''
                Programming Books
                \r1) Edit
                \r2) Delete
                \r3) Return to Main Menu''')      
        choice = input('What would you like to do?\n')
        if choice in ['1','2','3']:
            return choice
        else:
            print('Please choose one of the options below.\n'
            'A number from 1 - 3.')


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

def clean_id(id_str, options):
    try:
        book_id = int(id_str)
    except ValueError:
        input('''
        \n*****ID Error*****
              \rThe ID should be a number
              \rPress Enter to Try again.''')
        return
    else:
        if book_id in options:
            return book_id
        else:
            input(f'''
            \nID ERROR
            \rOptions: {options}
            \rPress enter to try again.
''')
            return

def edit_check(column_name, current_value):
    print(f'\n*** Edit {column_name} ***')
    if column_name == 'Price':
        print(f'\nCurrent Value: {current_value/100}')
    elif column_name == 'Date':
        print(f'\nCurrent Value: {current_value.strftime("%B %d, %Y")}')
    else:
        print(f'\nCurrent Value: {current_value}')
    if column_name == 'Date' or column_name == 'Price':
        while True:
            changes = input('What would you like to change the value to?')
            if column_name == 'Date':
                changes = clean_date(changes)
                if type(changes) == datetime.date:
                    return changes
            elif column_name == 'Price':
                changes = clean_price(changes)
                if type(changes) == int:
                    return changes
    else:
        return input('What would you like to change the value to?')

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
            id_options = []
            for book in session.query(Book):
                id_options.append(book.id)
            id_error = True
            while id_error:
                id_choice = input(f'''
                    \nId Options: {id_options}
                    \rBook ID: ''')
                id_choice = clean_id(id_choice, id_options)
                if type(id_choice) == int:
                    id_error = False
            the_book = session.query(Book).filter(Book.id==id_choice).first()
            print(f'\n{the_book.title} by {the_book.author} \nPublished: {the_book.published_date}\nPrice: ${the_book.price / 100}')
            sub_choice = int(submenu())
            if sub_choice == 1:
                the_book.title = edit_check('Title', the_book.title)
                the_book.author = edit_check('Author', the_book.author)
                the_book.published_date = edit_check('Date', the_book.published_date)
                the_book.price = edit_check('Price', the_book.price)
                session.commit()
                print('Book updated!')
                time.sleep(1.5)
            
            elif sub_choice == 2:
                session.delete(the_book)
                session.commit()
                print('Book deleted!')
                time.sleep(1.5)
        elif choice == '4':
            print('\n📚 BOOK ANALYSIS 📚\n' + '-'*40)

            oldest_book = session.query(Book).order_by(Book.published_date).first()
            newest_book = session.query(Book).order_by(Book.published_date.desc()).first()
            total_books = session.query(Book).count()
            python_books = session.query(Book).filter(Book.title.like("%Python%")).count()

            print(f"Total Books in Database: {total_books}")
            print(f"Books with 'Python' in Title: {python_books}\n")

            print(f"📖 Oldest Book:")
            print(f"   Title : {oldest_book.title}")
            print(f"   Author: {oldest_book.author}")
            print(f"   Date  : {oldest_book.published_date.strftime('%B %d, %Y')}\n")

            print(f"📖 Newest Book:")
            print(f"   Title : {newest_book.title}")
            print(f"   Author: {newest_book.author}")
            print(f"   Date  : {newest_book.published_date.strftime('%B %d, %Y')}\n")

            input('Press Enter to return to the main menu.')

        elif choice == '5':
            print('Good-bye')
            app_running = False


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app()
    # add_csv()
    for book in session.query(Book):
        print(book)