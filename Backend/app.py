from flask import request, json
from flask import Flask
from flask.views import MethodView
from extension import db,cors
from models import Book

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:19961006@localhost:3306/testdb?charset=utf8mb4'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
db.init_app(app)
cors.init_app(app)

@app.cli.command() # 自定义指令
def create():
    '''
    终端输入flask create即可初始化数据库
    :return:
    '''
    db.drop_all()   # 把旧的数据表全部删除
    db.create_all() # 创建一个新的数据表
    Book.init_db()  # 初始化数据

class BookApi(MethodView):
    def get(self,book_id):
        '''
        获取图书信息
        :param book_id:
        :return:
        '''
        # 如果没有指定ID，返回所有书籍
        if not book_id:
            books: [Book] = Book.query.all() # 类型注释，表示books是一个列表，列表中的元素都是Book元素
            results = [
                {
                    'id':book.id,
                    'book_name':book.book_name,
                    'book_type':book.book_type,
                    'book_prize':book.book_prize,
                    'book_number':book.book_number,
                    'book_publisher':book.book_publisher,
                    'author':book.author,
                } for book in books
            ] # 列表推导式
            ret = {
                'status' : 'success',
                'message' : '数据查询成功',
                'results': results
            }
        # 指定了ID，返回单本书
        else:
            book: Book = Book.query.get(book_id)
            ret= {
                'status': 'success',
                'message': '数据查询成功',
                'results': {
                    'id':book.id,
                    'book_name':book.book_name,
                    'book_type':book.book_type,
                    'book_prize':book.book_prize,
                    'book_number':book.book_number,
                    'book_publisher':book.book_publisher,
                    'author':book.author,
                }
            }
        # 返回中文
        return json.dumps(ret, ensure_ascii=False)

    def post(self):
        '''
        新增图书
        :return:
        '''
        form = request.json
        book = Book()
        book.book_number = form.get('book_number')
        book.book_name = form.get('book_name')
        book.book_type = form.get('book_type')
        book.book_prize = form.get('book_prize')
        book.author = form.get('author')
        book.book_publisher = form.get('book_publisher')
        db.session.add(book)
        db.session.commit()
        ret =  {
            'status': 'success',
            'message': '数据添加成功',
        }
        return json.dumps(ret, ensure_ascii=False)

    def delete(self,book_id):
        '''
        删除单本书
        :param book_id:
        :return:
        '''
        book = Book.query.get(book_id)
        db.session.delete(book)
        db.session.commit()
        ret = {
            'status': 'success',
            'message': '数据删除成功',
        }
        return json.dumps(ret, ensure_ascii=False)

    def put(self,book_id):
        '''
        数据库更新
        :param book_id:
        :return:
        '''
        book:Book = Book.query.get(book_id)
        book.book_number = request.json.get('book_number')
        book.book_name = request.json.get('book_name')
        book.book_type = request.json.get('book_type')
        book.book_prize = request.json.get('book_prize')
        book.author = request.json.get('author')
        book.book_publisher = request.json.get('book_publisher')
        db.session.commit()
        ret =  {
            'status': 'success',
            'message': '数据修改成功',
        }
        return json.dumps(ret, ensure_ascii=False)

book_view = BookApi.as_view('book_api')
# 注意斜杠问题
app.add_url_rule('/books/',
                 defaults={'book_id':None},
                 view_func=book_view,methods=['GET',])
app.add_url_rule('/books/',
                 view_func=book_view,methods=['POST',])
app.add_url_rule('/books/<int:book_id>',
                 view_func=book_view,
                 methods=['GET','PUT','DELETE'])

if __name__ == '__main__':
    app.run(debug=True)