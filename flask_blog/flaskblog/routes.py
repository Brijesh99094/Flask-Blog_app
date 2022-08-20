from flask import render_template,flash,redirect
from flaskblog.models import User,Post
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog import app,db,bcrypt
from flask_login import login_user


posts = [
    {
        'author':'Sanjay sathwara',
        'title':'Blog Post1',
        'content':'This is my first blog',
        'posted':'April 2021'
    },
     {
        'author':'Shyam patel',
        'title':'Blog Post2',
        'content':'This is my second blog',
        'posted':'May 2021'
    }
]


@app.route("/")
def hello():
    return render_template('home.html',posts=posts)


@app.route("/about")
def about():
     return render_template('about.html',title='About')


@app.route("/register",methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hased_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data,password=hased_pass)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created {form.username.data}!','success')
        return redirect('login')
    return render_template('register.html',title='Register',form=form)


@app.route("/login",methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print('hell')
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            return redirect('/')
        else:
            flash(f'Login unsuccesfull  Please check email and password!','danger')
    return render_template('login.html',title='Login',form=form)
