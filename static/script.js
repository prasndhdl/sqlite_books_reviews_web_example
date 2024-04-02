// Array to store book data
const books = [];

// Function to add a book to the list and send it to the server
function addBook() {
    const bookTitle = document.getElementById('bookTitle').value;
    const publicationYear = document.getElementById('publicationYear').value;
    let authorNames = document.getElementById('authorNames').value.split(','); // Get the author names as an array.

    // Create a JSON object with book data
    const bookData = {
        title: bookTitle,
        publication_year: publicationYear,
        author_names: authorNames // Include the author names as an array.
    };

    console.log(bookData);

    // Send the book data to the server via POST request
    fetch('/api/add_book', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(bookData)
    })
        .then(response => response.json())
        .then(data => {
            // Display a success message or handle errors if needed
            console.log(data.error);

            // Add the new book data to the books array
            books.push(bookData);
            console.log(books)

            // Refresh the book list
            displayBooks();
        })
        .catch(error => {
            console.error('Error adding book:', error);
        });
}

// Function to display books in the list
function displayBooks() {
    const bookList = document.getElementById('bookList');
    bookList.innerHTML = ''; // Clear existing book list

    books.forEach(book => {
        const bookElement = document.createElement('div');
        bookElement.innerHTML = `
            <h2>${book.title}</h2>
            <p>Author: ${book.author_names}</p> <!-- Display the author's name -->
            <p>Publication Year: ${book.publication_year}</p>
        `;
        bookList.appendChild(bookElement);
    });
}

// Function to fetch and display all books from the server
function showAllBooks() {
    fetch('/api/books')
        .then(response => response.json())
        .then(data => {
            const bookList = document.getElementById('allbooks');
            bookList.innerHTML = ''; // Clear existing book list
            console.log(data)
            data.books.forEach(book => { // Access the 'books' key in the JSON response
                const bookElement = document.createElement('div');
                bookElement.innerHTML = `
                    <h2>${book.title}</h2>
                    <p>Author: ${book.author_names}</p> <!-- Display the author's name -->
                    <p>Publication Year: ${book.publication_year}</p>
                `;
                bookList.appendChild(bookElement);
            });
        })
        .catch(error => {
            console.error('Error fetching all books:', error);
        });
}

