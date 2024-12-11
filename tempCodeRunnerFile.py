import datetime
import pickle

class Book:
    def __init__(self, book_id, title, author, category):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.category = category
        self.available = True  # Indicates if the book is available for borrowing

    def __str__(self):
        return f"{self.book_id}: {self.title} by {self.author} ({'Available' if self.available else 'Borrowed'})"


class User:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.borrowed_books = {}  # Dictionary to store borrowed books with return dates

    def __str__(self):
        return f"User {self.user_id}: {self.name} ({len(self.borrowed_books)} books borrowed)"

    def borrow_book(self, book, return_date):
        if len(self.borrowed_books) >= 3:  # Limit to 3 borrowed books
            print("You can only borrow up to 3 books.")
            return False
        self.borrowed_books[book.book_id] = return_date  # Store the book ID with its return date
        return True

    def return_book(self, book_id):
        if book_id in self.borrowed_books:
            del self.borrowed_books[book_id]  # Remove the book from borrowed list
            return True
        return False


class Library:
    def __init__(self):
        self.books = []  # List to hold all books in the library
        self.users = []  # List to hold all registered users
        self.load_data()  # Load data from file if it exists

    def save_data(self):
        """Save the current state of books and users to a file."""
        with open("library_data.pkl", "wb") as file:
            pickle.dump((self.books, self.users), file)

    def load_data(self):
        """Load the state of books and users from a file."""
        try:
            with open("library_data.pkl", "rb") as file:
                self.books, self.users = pickle.load(file)
        except FileNotFoundError:
            self.books = []
            self.users = []

    def add_book(self, title, author, category):
        """Add a new book to the library."""
        book_id = len(self.books) + 1  # Simple ID assignment based on current length
        book = Book(book_id, title, author, category)
        self.books.append(book)  # Add the new book to the list
        self.save_data()  # Save changes to file
        print(f"Book '{title}' added successfully!")

    def remove_book(self, book_id):
        """Remove a book from the library by its ID."""
        original_count = len(self.books)
        self.books = [book for book in self.books if book.book_id != book_id]
        
        if len(self.books) < original_count:  # If a book was removed
            self.save_data()  # Save changes to file
            print(f"Book {book_id} removed successfully!")
            return True
        
        print(f"Book {book_id} not found.")
        return False

    def list_books(self):
        """Return a list of all books in the library."""
        return self.books

    def search_books(self, keyword):
        """Search for books by title using a keyword."""
        return [book for book in self.books if keyword.lower() in book.title.lower()]

    def register_user(self, name, email):
        """Register a new user in the library."""
        user_id = len(self.users) + 1  # Simple ID assignment based on current length
        user = User(user_id, name, email)
        self.users.append(user)  # Add the new user to the list
        self.save_data()  # Save changes to file
        print(f"User '{name}' registered successfully!")

    def borrow_book(self, user_id, book_id):
        """Allow a user to borrow a book."""
        
        user = next((u for u in self.users if u.user_id == user_id), None)
        book = next((b for b in self.books if b.book_id == book_id), None)

        if user and book and book.available:
            return_date = datetime.date.today() + datetime.timedelta(days=14)  # Set return date to two weeks from now
            
            if user.borrow_book(book, return_date):  # Attempt to borrow the book
                book.available = False  # Mark the book as unavailable
                self.save_data()  # Save changes to file
                print(f"Book '{book.title}' borrowed successfully! Return by {return_date}.")
                return True
            
            print("Borrowing failed.")
        
        print("Invalid user or book ID, or the book is not available.")
        
        return False

    def return_book(self, user_id, book_id):
        """Allow a user to return a borrowed book."""
        
        user = next((u for u in self.users if u.user_id == user_id), None)
        
        if user and any(b.book_id == book_id for b in self.books): 
            if user.return_book(book_id):  # Attempt to return the borrowed book
                
                for book in self.books:
                    if book.book_id == book_id:
                        book.available = True  
                        break 
                
                self.save_data()  # Save changes to file
                print(f"Book '{book.title}' returned successfully!")
                return True
            
            print("Book not found in user's borrowed list.")
        
        print("Invalid user or book ID.")
        
        return False

    def get_borrowed_books(self, user_id):
        """Get all books borrowed by a specific user."""
        user = next((u for u in self.users if u.user_id == user_id), None)
    
        if user:
             return [self.get_book_by_id(book_id) for book_id in user.borrowed_books.keys()]

        return []  # Return an empty list if no user found


    def get_book_by_id(self, book_id):
        """Retrieve a book by its ID."""
        
        return next((b for b in self.books if b.book_id == book_id), None)