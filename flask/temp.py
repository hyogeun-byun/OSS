from flask import Flask, render_template

app = Flask(__name__, static_folder='templates/static')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/모범택시')
def mo():
     return render_template('모범택시.html', title='모범택시')

@app.route('/이미테이션')
def im():
     return render_template('이미테이션.html', title='이미테이션')

@app.route('/다크홀')
def dark():
     return render_template('다크홀.html', title='다크홀')

@app.route('/대박부동산')
def good():
     return render_template('대박부동산.html', title='대박부동산')

@app.route('/로스쿨')
def law():
     return render_template('로스쿨.html', title='로스쿨')

@app.route('/마인')
def mi():
     return render_template('마인.html', title='마인')

@app.route('/멸망')
def fall():
     return render_template('멸망.html', title='멸망')

@app.route('/미스몬테크리스토')
def miss():
     return render_template('미스몬테크리스토.html', title='미스몬테크리스토')

@app.route('/밥이되어라')
def bob():
     return render_template('밥이되어라.html', title='밥이되어라')

@app.route('/보쌈')
def bo():
     return render_template('보쌈.html', title='보쌈')

@app.route('/속아도꿈결')
def dream():
     return render_template('속아도꿈결.html', title='속아도꿈결')

@app.route('/아모르파티')
def party():
     return render_template('아모르파티.html', title='아모르파티')

@app.route('/언더커버')
def under():
     return render_template('언더커버.html', title='언더커버')

@app.route('/오월의청춘')
def five():
     return render_template('오월의청춘.html', title='오월의청춘')

@app.route('/오케이광자매')
def ok():
     return render_template('오케이광자매.html', title='오케이광자매')

@app.route('/about')
def about():
     return render_template('about.html', title='About')


if __name__ == '__main__':
    app.run()
