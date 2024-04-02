from flask import Flask, jsonify, render_template, request
import sqlite3

app = Flask(__name__)

# Define the path to your SQLite database file
DATABASE = 'C:/Users/prasn/Downloads/CSCI 514/sqlite_books_reviews_web_example/sqlite_books_reviews_web_example/db/books.db'

@app.route('/api/books', methods=['GET'])
def get_all_books():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(""" SELECT Booksv2.book_id, Booksv2.title, Booksv2.publication_year, Authors.author_name FROM 
                            (SELECT * FROM Books
                            LEFT JOIN book_authors
                            ON Books.book_id = book_authors.book_id) AS Booksv2 
                            LEFT JOIN Authors
                            ON Booksv2.author_id = Authors.author_id """)
        books = cursor.fetchall()
        conn.close()

        # Convert the list of tuples into a list of dictionaries
        book_list = []
        for book in books:
            book_dict = {
                'book_id': book[0],
                'title': book[1],
                'publication_year': book[2],
                'author_names' : book[3]
               
                # Add other attributes here as needed
            }
            book_list.append(book_dict)

        return jsonify({'books': book_list})
    except Exception as e:
        return jsonify({'error': str(e)})


# API to get all authors
@app.route('/api/authors', methods=['GET'])
def get_all_authors():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Authors")
        authors = cursor.fetchall()
        conn.close()
        return jsonify(authors)
    except Exception as e:
        return jsonify({'error': str(e)})

# API to get all reviews
@app.route('/api/reviews', methods=['GET'])
def get_all_reviews():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Reviews")
        reviews = cursor.fetchall()
        conn.close()
        return jsonify(reviews)
    except Exception as e:
        return jsonify({'error': str(e)})

# API to add a book to the database
@app.route('/api/add_book', methods=['POST'])
def add_book():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Get book details from the request
        data = request.get_json()
        title = data.get('title')
        publication_year = data.get('publication_year')
        print(title)
        author_names = data.get('author_names')  # Retrieve the author names as a list from the requested data.

        book_id = hash(title + publication_year)

        # Insert the book into the database
        
        cursor.execute("INSERT INTO Books (book_id, title, publication_year ) VALUES (?, ?, ?)", (book_id, title, publication_year,))
            # book_ids.append(cursor.lastrowid)  # Get the ID of the newly inserted book
       
          # Insert the authors into the Authors table if they don't exist and get their IDs
        author_ids = []
        for author in author_names:
            cursor.execute("SELECT author_id FROM Authors WHERE author_name = ?", (author,))
            author_row = cursor.fetchone()

            if author_row:
                author_ids.append(author_row[0])
            else:
                # If the author doesn't exist, insert them into the Authors table
                cursor.execute("INSERT INTO Authors (author_name) VALUES (?)", (author,))
                author_id = cursor.lastrowid
            author_ids.append(author_id)

        # Establish the relationship between the book and authors in the book_author table
        for id in author_ids:
            cursor.execute("INSERT INTO book_authors (book_id, author_id) VALUES (?, ?)", (book_id,id,))
        
        conn.commit()
        conn.close()

        return jsonify({'message': 'Book added successfully with the author name'})
    except Exception as e:
        return jsonify({'error': str(e)})

# Route to render the index.html page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
