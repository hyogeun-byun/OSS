from flask import Flask, render_template
import pymysql


class Database():
    # DB 연결
    def __init__(self):           
        self.db = pymysql.connect(host='localhost',
                                  user='findrama',
                                  password='findrama',
                                  db='findrama',
                                  charset='utf8')
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
    
    # sql문 실행
    def execute(self, query, args={}):
        self.cursor.execute(query, args)
        
    # sql문 실행하여 1개의 tuple fetch
    def executeOne(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchone()
        return row
    # sql문 실행하여 전체 tuple fetch
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

    return render_template('home.html', resultData=row)

# 각 드라마 별로 DB 연결

@app.route('/이미테이션')
def info_0():
    db_class = Database()

    sql = "SELECT * \
                FROM drama WHERE id = 0"
    row = db_class.executeAll(sql)

    sql_actor = "SELECT * FROM actor WHERE id = 0"
    actors = db_class.executeAll(sql_actor)

    return render_template('이미테이션.html', resultData=row[0], actor = actors)

@app.route('/멸망')
def info_1():
    db_class = Database()

    sql = "SELECT * \
                FROM drama WHERE id = 1"
    row = db_class.executeAll(sql)

    sql_actor = "SELECT * FROM actor WHERE id = 1"
    actors = db_class.executeAll(sql_actor)

    return render_template('멸망.html', resultData=row[0], actor = actors)

@app.route('/오월의청춘')
def info_2():
    db_class = Database()

    sql = "SELECT * \
                FROM drama WHERE id = 2"
    row = db_class.executeAll(sql)
    sql_actor = "SELECT * FROM actor WHERE id = 2"
    actors = db_class.executeAll(sql_actor)
    return render_template('오월의청춘.html', resultData=row[0], actor = actors)

@app.route('/로스쿨')
def info_3():
    db_class = Database()

    sql = "SELECT * \
                FROM drama WHERE id = 3"
    row = db_class.executeAll(sql)
    sql_actor = "SELECT * FROM actor WHERE id = 3"
    actors = db_class.executeAll(sql_actor)
    return render_template('로스쿨.html', resultData=row[0], actor = actors)

@app.route('/대박부동산')
def info_4():
    db_class = Database()

    sql = "SELECT * \
                FROM drama WHERE id = 4"
    row = db_class.executeAll(sql)
    sql_actor = "SELECT * FROM actor WHERE id = 4"
    actors = db_class.executeAll(sql_actor)
    return render_template('대박부동산.html', resultData=row[0], actor = actors)

@app.route('/모범택시')
def info_5():
    db_class = Database()

    sql = "SELECT * \
                FROM drama WHERE id = 5"
    row = db_class.executeAll(sql)
    sql_actor = "SELECT * FROM actor WHERE id = 5"
    actors = db_class.executeAll(sql_actor)
    return render_template('모범택시.html', resultData=row[0], actor = actors)

@app.route('/다크홀')
def info_6():
    db_class = Database()

    sql = "SELECT * \
                FROM drama WHERE id = 6"
    row = db_class.executeAll(sql)
    sql_actor = "SELECT * FROM actor WHERE id = 6"
    actors = db_class.executeAll(sql_actor)

    return render_template('다크홀.html', resultData=row[0], actor = actors)

@app.route('/언더커버')
def info_7():
    db_class = Database()

    sql = "SELECT * \
                FROM drama WHERE id = 7"
    row = db_class.executeAll(sql)
    sql_actor = "SELECT * FROM actor WHERE id = 7"
    actors = db_class.executeAll(sql_actor)

    return render_template('언더커버.html', resultData=row[0], actor = actors)

@app.route('/오케이광자매')
def info_8():
    db_class = Database()

    sql = "SELECT * \
                FROM drama WHERE id = 8"
    row = db_class.executeAll(sql)
    sql_actor = "SELECT * FROM actor WHERE id = 8"
    actors = db_class.executeAll(sql_actor)

    return render_template('오케이광자매.html', resultData=row[0], actor = actors)

@app.route('/마인')
def info_9():
    db_class = Database()

    sql = "SELECT * \
                FROM drama WHERE id = 9"
    row = db_class.executeAll(sql)
    sql_actor = "SELECT * FROM actor WHERE id = 9"
    actors = db_class.executeAll(sql_actor)

    return render_template('마인.html', resultData=row[0], actor = actors)

@app.route('/보쌈')
def info_10():
    db_class = Database()

    sql = "SELECT * \
                FROM drama WHERE id = 10"
    row = db_class.executeAll(sql)
    sql_actor = "SELECT * FROM actor WHERE id = 10"
    actors = db_class.executeAll(sql_actor)

    return render_template('보쌈.html', resultData=row[0], actor = actors)

@app.route('/아모르파티')
def info_11():
    db_class = Database()

    sql = "SELECT * \
                FROM drama WHERE id = 11"
    row = db_class.executeAll(sql)
    sql_actor = "SELECT * FROM actor WHERE id = 11"
    actors = db_class.executeAll(sql_actor)

    return render_template('아모르파티.html', resultData=row[0], actor = actors)

@app.route('/밥이되어라')
def info_12():
    db_class = Database()

    sql = "SELECT * \
                FROM drama WHERE id = 12"
    row = db_class.executeAll(sql)
    sql_actor = "SELECT * FROM actor WHERE id = 12"
    actors = db_class.executeAll(sql_actor)

    return render_template('밥이되어라.html', resultData=row[0], actor = actors)

@app.route('/미스몬테크리스토')
def info_13():
    db_class = Database()

    sql = "SELECT * \
                FROM drama WHERE id = 13"
    row = db_class.executeAll(sql)
    sql_actor = "SELECT * FROM actor WHERE id = 13"
    actors = db_class.executeAll(sql_actor)

    return render_template('미스몬테크리스토.html', resultData=row[0], actor = actors)

@app.route('/속아도꿈결')
def info_14():
    db_class = Database()

    sql = "SELECT * \
                FROM drama WHERE id = 14"
    row = db_class.executeAll(sql)
    sql_actor = "SELECT * FROM actor WHERE id = 14"
    actors = db_class.executeAll(sql_actor)


    return render_template('속아도꿈결.html', resultData=row[0], actor = actors)
# 여기까지 추가

if __name__=='__main__':
    app.run(debug=True)

from app import app
