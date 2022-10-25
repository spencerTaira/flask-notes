from flask import Flask, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import RegisterForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'our secret'

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///notes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)
db.create_all()

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

@app.get('/')
def root():
    """ Redirects to /register """

    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register():

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register()
        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.username

        return redirect('/secret')

    else:
        return render_template('register.html', form=form)

@app.get('/secret')