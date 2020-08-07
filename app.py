from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Collection
from forms import UserLoginForm, UserSignupForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgres:///cardboardroster_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

@app.route('/')
def go_to_signup():
    return redirect('/signup')

@app.route('/signup', methods=['GET', 'POST'])
def show_signup():
    form = UserSignupForm()
    if form.validate_on_submit():
        new_user = User.register(username=form.username.data, 
                                 password=form.password.data, 
                                 email=form.email.data, 
                                 first_name=form.first_name.data, 
                                 last_name=form.last_name.data)
        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
    return render_template('signup.html', form=form)