from flask import Flask, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import CSRFProtectForm, RegisterForm, LoginForm

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

        user = User.register(username, password, email, first_name, last_name)
        db.session.add(user)
        db.session.commit()

        session['username'] = user.username

        return redirect(f'/users/{user.username}')

    else:
        return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Produce login form or handle form"""

    form = LoginForm()

    if form.validate_on_submit():
        name = form.username.data
        password = form.password.data

        user = User.authenticate(name, password)

        if user:
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ["Incorrect username/password"]

    return render_template("login.html", form=form)


@app.get('/users/<username>')
def show_user_detail(username):
    """Example of hidden page for logged-in users only """

    form = CSRFProtectForm()
    user = User.query.get_or_404(username)

    if session.get('username') != username:
        flash("You must be logged in to view!")
        return redirect('/')

    else:
        return render_template("user_detail.html", form=form, user=user)

@app.post('/logout')
def logout():
    """ Logs user out and redirects to homepage """

    form = CSRFProtectForm()

    if form.validate_on_submit():
        # Remove "username" if present, but no errors if it isn't
        session.pop('username', None)
        print('LOGOGOGOGOGOGOGOGOOGOoooOOOOOOO!!!!!!!!!!!!!!!!')
    return redirect('/')