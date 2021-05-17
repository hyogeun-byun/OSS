from flask import Flask, render_template

app = Flask(__name__, static_folder='templates/static')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/모범택시')
def mo():
     return render_template('모범택시.html', title='모범택시')

@app.route('/이미테이션')
def bin():
     return render_template('이미테이션.html', title='이미테이션')

@app.route('/about')
def about():
     return render_template('about.html', title='About')

if __name__ == '__main__':
    app.run()
