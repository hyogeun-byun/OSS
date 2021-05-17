from flask import Flask, render_template
#from app import mod_dbconn
import pymysql


class Database():
    def __init__(self):
        self.db = pymysql.connect(host='localhost',
                                  user='findrama',
                                  password='findrama',
                                  db='findrama',
                                  charset='utf8')
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

    def execute(self, query, args={}):
        self.cursor.execute(query, args)

    def executeOne(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchone()
        return row

    def executeAll(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        return row

    def commit(self):
        self.db.commit()


app = Flask(__name__,static_folder='templates/static')


@app.route('/')
def home(): 
    db_class = Database()

    sql = "SELECT * \
                FROM drama"
    row = db_class.executeAll(sql)

    return render_template('home.html', resultData=row[0])


# 여기부터 추가
@app.route('/빈센조')
def select():
    db_class = Database()

    sql = "SELECT * \
                FROM drama WHERE id = 0"
    row = db_class.executeAll(sql)

    print(row)

    return render_template('빈센조.html', resultData=row[0])

# 여기까지 추가

if __name__=='__main__':
    app.run(debug=True)

from app import app