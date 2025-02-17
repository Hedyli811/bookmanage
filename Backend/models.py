from extension import db


class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_number = db.Column(db.String(255), nullable=False)
    book_name = db.Column(db.String(255), nullable=False)
    book_type = db.Column(db.String(255), nullable=False)
    book_price = db.Column(db.Float, nullable=False)
    author = db.Column(db.String(255))
    book_publisher = db.Column(db.String(255))

    @staticmethod
    def init_db():
        """
        Initialize the database with some default entries.
        :return: None
        """
        rets = [
            (1, '001', 'To Live', 'Fiction', 39.9, 'Yu Hua', 'Some Publisher'),
            (2, '002', 'The Three-Body Problem', 'Science Fiction', 99.8, 'Liu Cixin', 'Chongqing Publisher')
        ]

        for ret in rets:
            book = Book()
            book.id = ret[0]
            book.book_number = ret[1]
            book.book_name = ret[2]
            book.book_type = ret[3]
            book.book_price = ret[4]
            book.author = ret[5]
            book.book_publisher = ret[6]

            # Add the book instance to the session and commit
            db.session.add(book)

        db.session.commit()
