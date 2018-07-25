from flask import Flask, request, redirect, render_template,session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi
import os

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/Blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

@app.route('/newblog', methods=['POST', 'GET'])
def new_blog():
    owner = User.query.filter_by(email =session['email']).first()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if title != "" and content !="":
            new_blog = Blog(title, content)
            db.session.add(new_blog)
            db.session.commit()
            blog = Blog.query.filter_by(id=new_blog.id, owner = owner).first() 
            return render_template('entry.html', blog=blog, owner = owner)
           
        else:
            flash('Nothing entered','error')

    return render_template('newblog.html')
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blog = db.relationship('Blog', backref = 'owner')
    #owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self, email, password,owner):
        self.email = email
        self.password = password
        self.owner = owner
    
   # def __repr__(self):
        #return '<User %r>' % self.email

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self,title,content,owner):
        self.title = title
        self.content = content
        self.owner = owner
        


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('newblog.html', 
        blog=blog)


@app.route('/blog', methods = ['GET'])
def blog():
    owner = request.args.get('user')
    if owner:
        blogs = Blog.query.filter_by(owner_id=owner).all()
    id = request.args.get('/blog={{blog.id}}')
    blogs = Blog.query.all()
    return render_template('blog.html', blogs= blogs, owner = owner)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        users = User.query.filter_by(email=email)
        if users.count() == 1:
            user = users.first()
            if password == user.password:
                session['user'] = user.email
                flash('welcome back, '+user.email)
                return redirect("/")
        flash('bad email or password')
        return redirect("/login")

@app.route("/register", methods=['GET', 'POST'])
def register():
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']
        owner = request.args.get('user')
        if not is_email(email):
            flash('zoiks! "' + email + '" does not seem like an email address')
            return redirect('/register')
        #email_db_count = User.query.filter_by(email=email).count()
       # if email_db_count > 0:
            #flash('yikes! "' + email + '" is already taken and password reminders are not implemented')
            #return redirect('/register')
        if password != verify:
            flash('passwords did not match')
            return redirect('/register')
        user = User(email=email, password=password, owner = owner)
        db.session.add(user)
        db.session.commit()
        session['user'] = user.email
        return redirect("/")
    else:
        return render_template('register.html')

def is_email(string):
    atsign_index = string.find('@')
    atsign_present = atsign_index >= 0
    if not atsign_present:
        return False
    else:
        domain_dot_index = string.find('.', atsign_index)
        domain_dot_present = domain_dot_index >= 0
        return domain_dot_present

@app.route("/logout", methods=['POST'])
def logout():
    del session['user']
    return redirect("/")

app.secret_key = "kPmIIcAYqyJhc6TJQK7j"

if __name__ == '__main__':
    app.run()