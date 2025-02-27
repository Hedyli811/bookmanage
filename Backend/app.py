from flask import request, \
    json  # Import request for handling incoming HTTP requests and json for JSON data manipulation
from flask import Flask  # Importing the Flask class to create a Flask application
from flask.views import MethodView  # Import MethodView to create class-based views
from extension import db, cors  # Import the db and CORS instances initialized in the extension module
from models import Book  # Import the Book model which represents the book table in the database

# Create an instance of the Flask application
app = Flask(__name__)

# Set up the database connection; using MySQL with PyMySQL as the driver.
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:19961006@localhost:3306/testdb?charset=utf8mb4'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False  # Disable auto-commit after each request

# Initialize the db and CORS instances with the app configuration
db.init_app(app)
cors.init_app(app)


@app.cli.command()  # Define a custom command to be used in the CLI
def create():
    '''
    This function initializes the database.
    Run `flask create` in the terminal to execute this function.
    '''
    db.drop_all()  # Drop all existing tables in the database
    db.create_all()  # Create new tables according to the defined models
    Book.init_db()  # Call the method to populate the database with initial data


class BookApi(MethodView):
    def get(self, book_id):
        '''
        Retrieve book information based on the provided book_id.
        If no book_id is specified, return all books.
        :param book_id: The ID of the book to retrieve
        :return: A JSON response with book data
        '''
        # If no book ID is specified, fetch and return all books from the database
        if not book_id:
            # Retrieve all books and annotate the type for clarity
            books: [Book] = Book.query.all()

            # Construct the results in JSON format
            results = [
                {
                    'id': book.id,
                    'book_name': book.book_name,
                    'book_type': book.book_type,
                    'book_price': book.book_price,
                    'book_number': book.book_number,
                    'book_publisher': book.book_publisher,
                    'author': book.author,
                } for book in books
            ]  # Using list comprehension to create a list of dictionaries

            # Prepare the final response
            ret = {
                'status': 'success',
                'message': 'Data retrieved successfully',
                'results': results
            }
        # If a book ID is provided, fetch that specific book
        else:
            book: Book = Book.query.get(book_id)  # Fetch the book with the specified ID
            # Construct the response for a single book
            ret = {
                'status': 'success',
                'message': 'Data retrieved successfully',
                'results': {
                    'id': book.id,
                    'book_name': book.book_name,
                    'book_type': book.book_type,
                    'book_price': book.book_price,
                    'book_number': book.book_number,
                    'book_publisher': book.book_publisher,
                    'author': book.author,
                }
            }

        # Return the response in JSON format, ensuring proper character encoding
        return json.dumps(ret, ensure_ascii=False)

    def post(self):
        '''
        Add a new book to the database based on incoming JSON data.
        :return: A JSON response indicating success or failure
        '''
        form = request.json  # Parse the incoming JSON request body
        book = Book()  # Create an instance of the Book model

        # Assign values from the parsed JSON to the book instance
        book.book_number = form.get('book_number')
        book.book_name = form.get('book_name')
        book.book_type = form.get('book_type')
        book.book_price = form.get('book_price')
        book.author = form.get('author')
        book.book_publisher = form.get('book_publisher')

        db.session.add(book)  # Add the book instance to the current database session
        db.session.commit()  # Commit the transaction to save changes to the database

        # Prepare a success response
        ret = {
            'status': 'success',
            'message': 'Data added successfully',
        }
        return json.dumps(ret, ensure_ascii=False)  # Return the response in JSON format

    def delete(self, book_id):
        '''
        Delete a single book from the database based on book_id.
        :param book_id: The ID of the book to be deleted
        :return: A JSON response indicating success or failure
        '''
        book = Book.query.get(book_id)  # Retrieve the book by ID
        db.session.delete(book)  # Remove the book from the database session
        db.session.commit()  # Commit the transaction

        # Prepare a success response
        ret = {
            'status': 'success',
            'message': 'Data deleted successfully',
        }
        return json.dumps(ret, ensure_ascii=False)  # Return the response in JSON format

    def put(self, book_id):
        '''
        Update an existing book's details in the database based on book_id.
        :param book_id: The ID of the book to update
        :return: A JSON response indicating success or failure
        '''
        book: Book = Book.query.get(book_id)  # Retrieve the book by ID

        # Update book attributes from incoming JSON data
        book.book_number = request.json.get('book_number')
        book.book_name = request.json.get('book_name')
        book.book_type = request.json.get('book_type')
        book.book_price = request.json.get('book_price')
        book.author = request.json.get('author')
        book.book_publisher = request.json.get('book_publisher')

        db.session.commit()  # Commit the changes to the database

        # Prepare a success response
        ret = {
            'status': 'success',
            'message': 'Data modified successfully',
        }
        return json.dumps(ret, ensure_ascii=False)  # Return the response in JSON format


# 2.Convert the BookApi class into a view function that can be used with Flask routes
book_view = BookApi.as_view('book_api')

# Define URL rules for the book API endpoints
app.add_url_rule('/books/',
                 defaults={'book_id': None},  # Default value if no ID is specified
                 view_func=book_view, methods=['GET', ])  # GET method for retrieving books
app.add_url_rule('/books/',
                 view_func=book_view, methods=['POST', ])  # POST method for adding a new book
app.add_url_rule('/books/<int:book_id>',
                 view_func=book_view,  # Map to the BookApi view
                 methods=['GET', 'PUT', 'DELETE'])  # Allow GET, PUT, and DELETE method for a specific book

# If this script is run directly, start the Flask application in debug mode
if __name__ == '__main__':
    app.run(debug=True)