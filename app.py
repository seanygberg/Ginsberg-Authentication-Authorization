from flask import Flask, render_template, redirect, session
from models import db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm, DeleteForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'

db.init_app(app)

@app.route('/')
def home():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            password=form.password.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )
        db.session.add(user)
        db.session.commit()
        session['username'] = user.username
        return redirect('/secret')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            session['username'] = user.username
            return redirect('/secret')
    return render_template('login.html', form=form)

@app.route('/secret')
def secret():
    return redirect('/users/<username>')

@app.route('/users/<username>')
def user_detail(username):
    if 'username' not in session or session['username'] != username:
        return redirect('/login')
    user = User.query.get_or_404(username)
    return render_template('user_detail.html', user=user)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    if 'username' not in session or session['username'] != username:
        return redirect('/login')
    form = FeedbackForm()
    if form.validate_on_submit():
        feedback = Feedback(
            title=form.title.data,
            content=form.content.data,
            username=username
        )
        db.session.add(feedback)
        db.session.commit()
        return redirect(f'/users/{username}')
    return render_template('add_feedback.html', form=form)