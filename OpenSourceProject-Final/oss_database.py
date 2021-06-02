import pymysql

class Database():
    def __init__(self):
        self.db = pymysql.connect(host='localhost',
                                  user='root',
                                  password='byun0424',
                                  db='findrama',
                                  charset='utf8')
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

    def execute(self, query, args={}):                          # sql문 실행
        self.cursor.execute(query, args)

    def executeOne(self, query, args={}):                       # 하나의 tuple fectch
        self.cursor.execute(query, args)
        row = self.cursor.fetchone()
        return row

    def executeAll(self, query, args={}):                       # 전체 tuple fectch
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        return row

    def commit(self):
        self.db.commit()

