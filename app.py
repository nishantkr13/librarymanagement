from flask import Flask, render_template, redirect, url_for, request, flash
from library import Library

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages
library = Library()

# Route for the homepage (index)
@app.route('/')
def index():
    user_id = 1  # Replace with actual logic to fetch logged-in user ID
    borrowed_books = library.get_borrowed_books(user_id)  # Fetch borrowed books for this user
    return render_template('index.html', borrowed_books=borrowed_books)

# Route to view books
@app.route('/view_books')
def view_books():
    books = library.list_books()  # Get list of books
    return render_template('books.html', books=books)

# Route to remove a book
@app.route('/remove_book/<int:book_id>', methods=['GET'])
def remove_book_route(book_id):
    try:
        library.remove_book(book_id)
        flash(f'Book {book_id} removed successfully!')
    except Exception as e:
        flash(f'Error removing book: {str(e)}')
    return redirect(url_for('view_books'))

# Route to borrow a book
@app.route('/borrow_book/<int:book_id>', methods=['GET'])
def borrow_book_route(book_id):
    user_id = 1  # Replace with actual logic to fetch logged-in user ID
    result = library.borrow_book(user_id, book_id)  # Attempt to borrow the book
    if result:
        flash(f'You have borrowed the book successfully!')
    else:
        flash(f'Failed to borrow book {book_id}. It may be unavailable or you have reached your limit.')
    return redirect(url_for('view_books'))

# Route to add a new book
@app.route('/add_book', methods=['GET', 'POST'])
def add_book_route():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        category = request.form['category']
        library.add_book(title, author, category)
        flash(f'Book "{title}" added successfully!')
        return redirect(url_for('view_books'))
    return render_template('add_book.html')

# Route to search for books
@app.route('/search_books', methods=['GET', 'POST'])
def search_books_route():
    if request.method == 'POST':
        keyword = request.form['keyword']
        books = library.search_books(keyword)
        return render_template('books.html', books=books)
    return render_template('search_books.html')

# Route to register a new user
@app.route('/register_user', methods=['GET', 'POST'])
def register_user_route():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        library.register_user(name, email)
        flash(f'User "{name}" registered successfully!')
        return redirect(url_for('index'))
    return render_template('register_user.html')

# Route to return a borrowed book
@app.route('/return_book/<int:book_id>', methods=['GET'])
def return_book_route(book_id):
    user_id = 1  # Replace with actual logic to fetch logged-in user ID
    result = library.return_book(user_id, book_id)  # Attempt to return the book
    if result:
        flash(f'Book {book_id} returned successfully!')
    else:
        flash(f'Failed to return book {book_id}. It may not be in your borrowed list.')
    return redirect(url_for('view_books'))
# Route to view borrowed books
@app.route('/view_borrowed_books')
def view_borrowed_books():
    user_id = 1  # Replace with actual logic to fetch logged-in user ID
    borrowed_books = library.get_borrowed_books(user_id)
    print(f"Borrowed Books for User {user_id}: {borrowed_books}")  # Debugging output
    return render_template('borrowed_books.html', borrowed_books=borrowed_books)

@app.route('/remove_borrowed_book/<int:book_id>', methods=['POST'])
def remove_borrowed_book(book_id):
    user_id = 1  # Replace with actual logic to fetch logged-in user ID
    result = library.return_book(user_id, book_id)  # Use return_book method to remove from borrowed list
    if result:
        flash(f'Book "{book_id}" removed from your borrowed list successfully!')
    else:
        flash(f'Failed to remove book "{book_id}". It may not be in your borrowed list.')
    
    return redirect(url_for('view_borrowed_books'))

if __name__ == '__main__':
    app.run(debug=True)