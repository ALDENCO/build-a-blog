from flask import Flask, request, redirect, render_template,session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/Blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

@app.route('/newblog', methods=['POST', 'GET'])
def new_blog():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if title != "" and content !="":
            new_blog = Blog(title, content)
            db.session.add(new_blog)
            db.session.commit()
            blog = Blog.query.filter_by(id=new_blog.id).first() 
            return render_template('entry.html', blog=blog)
           
        else:
            flash('Nothing entered','error')

    return render_template('newblog.html')
    
    
class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.Text)

    def __init__(self, title,content):
        self.title = title
        self.content = content


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('newblog.html', 
        blog=blog)


@app.route('/blog', methods = ['GET'])
def blog():
    id = request.args.get('blog')
    blog = Blog.query.filter_by(id=id).first()
    return render_template('blog.html', blog= blog)

@app.route('/entry', methods=['GET'])
def entry():
   blogs = Blog.query.all()
   return render_template('blog.html',
        blogs=blogs)
    



if __name__ == '__main__':
    app.run()