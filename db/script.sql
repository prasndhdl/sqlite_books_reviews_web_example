CREATE TABLE Authors (
author_id INTEGER PRIMARY KEY,
author_name TEXT NOT NULL
);

CREATE TABLE Books (
book_id INTEGER PRIMARY KEY,
title TEXT NOT NULL,
publication_year INTEGER
);





CREATE TABLE IF NOT EXISTS Users (
user_id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Reviews (
review_id INTEGER PRIMARY KEY,
book_id INTEGER NOT NULL,
user_id INTEGER NOT NULL,
rating INTEGER,
review_text TEXT,
review_date DATE,
FOREIGN KEY (book_id) REFERENCES Books (book_id),
FOREIGN KEY (user_id) REFERENCES Users (user_id)
);

CREATE TABLE book_authors (
book_id INTEGER NOT NULL,
author_id INTEGER NOT NULL,
PRIMARY KEY (book_id, author_id),
FOREIGN KEY (book_id) REFERENCES Books (book_id),
FOREIGN KEY (author_id) REFERENCES Authors (author_id)

);


------------------

PRAGMA table_info([Books]);
PRAGMA table_info([Authors]);
PRAGMA table_info([book_authors]);
SELECT * FROM Books;
SELECT  * FROM Authors;
SELECT * FROM book_authors;


INSERT INTO BOOKS (book_id, title, publication_year, author_name) VALUES (1, "harryporter", 2005, "prashant");

DROP TABLE Books;
DROP TABLE Authors;
DROP TABLE book_authors;

SELECT Booksv2.book_id, Booksv2.title, Booksv2.publication_year, Authors.author_name FROM 
 (SELECT * FROM Books
LEFT JOIN book_authors
ON Books.book_id = book_authors.book_id) AS Booksv2 
LEFT JOIN Authors
ON Booksv2.author_id = Authors.author_id
;

