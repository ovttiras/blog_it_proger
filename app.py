from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import  datetime
from urllib.parse import quote as url_quote
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///blog.db'
db=SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
def __repr__(self):
    return '<Article %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/post')
def post():
    articles =Article.query.order_by(Article.date.desc()).all()
    return render_template('post.html', articles=articles)

@app.route('/post/<int:id>')
def post_detail(id):
    article =Article.query.get(id)
    return render_template('post_detail.html', article=article)

@app.route('/post/<int:id>/del')
def post_delete(id):
    article =Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/post')
    except:
        return 'При удалении статьи произошла ошибка'


@app.route('/post/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = Article.query.get(id)
    if request.method=='POST':
        article.title= request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']
        try:
            db.session.commit()
            return redirect('/post')
        except:
            return 'При редактировании статьи произошла ошибка'
    else:
        return render_template('post_update.html', article=article)


@app.route('/create_article', methods=['POST', 'GET'])
def create_article():
    if request.method=='POST':
        title= request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title,intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/post')
        except:
            return 'При добавлении статьи произошла ошибка'
    else:
        return render_template('create_article.html')

if __name__=='__main__':
    app.run(debug=True)
