from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(80), unique=True)
    author = db.Column('author', db.String(80))
    year = db.Column('year', db.Integer)
    active = db.Column('active', db.Boolean)


@app.route('/', methods=['GET'])
def get_books():
    books = Book.query.all()
    books_dict_list = list(map(lambda book: {'id': book.id, 'name': book.name,
                                             'author': book.author, 'year': book.year, 'active': book.active}, books))
    return jsonify(books_dict_list)


@app.route('/', methods=['POST'])
def add_book():
    if request.method == 'POST' and request.is_json:
        try:
            json_object = request.json
            book = Book()
            book.name = json_object['name']
            book.author = json_object['author']
            book.year = json_object['year']
            book.active = json_object['active']
            db.session.add(book)
            db.session.commit()
            return 'success'
        except Exception as error:
            return make_response(str(error.__cause__), 400)
    else:
        return make_response('fail', 400)


@app.route('/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    if request.method == 'PUT' and request.is_json:
        json_object = request.json
        try:
            book = Book()
            book.id = book_id
            book.name = json_object['name']
            book.author = json_object['author']
            book.year = json_object['year']
            book.active = json_object['active']
            db.session.merge(book)
            db.session.commit()
            return 'success'
        except Exception as error:
            return make_response(str(error.__cause__), 400)
    else:
        return make_response('fail', 400)


@app.route('/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    if request.method == 'DELETE':
        book = Book.query.filter(Book.id==book_id).scalar()
        if book is None:
            return make_response('book not found',404)
        else:
            db.session.delete(book)
            db.session.commit()
            return 'success'



if __name__ == '__main__':
    app.run(host='localhost', port=3000, debug=True)
