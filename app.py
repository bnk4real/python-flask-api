from flask import Flask, jsonify, request
from books import Books 

app = Flask(__name__)

# get all books (READ)
@app.route('/api/books', methods=['GET'])
def get_books():
    return jsonify(Books.books)

# get a specific book by ID
@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((book for book in Books.books if book['id'] == book_id), None)
    if book:
        return jsonify(book)
    else:
        return jsonify({"message": "Book not found"}), 404

# add a new book (CREATE)
@app.route('/api/books', methods=['POST'])
def add_book():
    new_book = request.get_json()
    if not new_book or 'title' not in new_book or 'author' not in new_book:
        return jsonify({"message": "Invalid request"}), 400
    new_book['id'] = len(Books.books) + 1 
    Books.books.append(new_book)
    return jsonify(new_book), 200

# update an existing book (UPDATE)
@app.route('/api/books/<int:book_id>', methods=['POST'])
def update_book(book_id):
    book = next((book for book in Books.books if book['id'] == book_id), None)
    if not book:
        return jsonify({"message": "Book not found"}), 404
    data = request.get_json()
    book.update(data)
    return jsonify(book), 200

# delete a book (DELETE)
@app.route('/api/books/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    global books
    Books.books = [book for book in Books.books if book['id'] != book_id]
    return jsonify({"message": "Book deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
