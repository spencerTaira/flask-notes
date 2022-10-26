from flask import Flask, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Note
from forms import CSRFProtectForm, RegisterForm, LoginForm, AddNotesForm, \
    EditNotesForm
from werkzeug.exceptions import Unauthorized


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
    """ GET: Renders register.html
        POST: Registers user if info is valid, adds session cookie with username,
        and redirects to /users/<username>
    """
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
    """GET: Renders login.html form
       POST: validates login info and if valid add session cookie wiht username,
       and redirects to /users/<usersname>
    """

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
            #Fall through to render_template
    return render_template("login.html", form=form)


@app.get('/users/<username>')
def show_user_detail(username):
    """Example of hidden page for logged-in users only
    If logged in, shows user info and has logout button.
    Else redirects to root and shows flashed message
    """


    form = CSRFProtectForm()
    user = User.query.get_or_404(username)
    notes = user.notes

    if session.get('username') != username:
        flash("You must be logged in to view!")
        return redirect('/')

    else:
        return render_template("user_detail.html", form=form, user=user, notes=notes)

@app.post('/logout')
def logout():
    """ Logs user out and redirects to homepage
        Logs out user by removing session cookie with username and redirects to
        root
    """

    form = CSRFProtectForm()

    if form.validate_on_submit():
        # Remove "username" if present, but no errors if it isn't
        session.pop('username', None)
    return redirect('/')

@app.route('/users/<username>/notes/add', methods=['GET', 'POST'])
def add_note(username):
    """GET: Displays a form to add a note to the database
       POST: Gets form data for new note and adds to the database.
       If invalid input, redirect to users/username.
       """

    form = AddNotesForm()

    if session.get('username') != username:
        # flash("You must be logged in to view!")
        raise Unauthorized()

        # return redirect('/')

    else:
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data

            user = User.query.get_or_404(username)
            note = Note(title=title, content=content, owner=user.username)

            db.session.add(note)
            db.session.commit()

            return redirect(f'/users/{username}')

        else:
            return render_template('add_note.html', form=form)

@app.post('/notes/<note_id>/delete')
def note_delete(note_id):
    """ Deletes note with note_id from table and redirects to
        /users/<username>
    """

    form = CSRFProtectForm()
    #add session protection

    if form.validate_on_submit():
        note = Note.query.get_or_404(note_id)
        username = note.user.username
        db.session.delete(note)
        db.session.commit()

        flash('Note has been deleted!')
        #fall through to redirect
    return redirect(f'/users/{username}')

@app.route('/notes/<note_id>/edit', methods=['GET', 'POST'])
def note_edit(note_id):
    """
    GET: Show edit note form filled with note data
    POST: Update table data with form data and redirect to /users/<username>
    """

    note = Note.query.get(note_id)
    form = EditNotesForm(obj=note)

    if session.get('username') != note.user.username:
        flash("You must be logged in to view!")
        return redirect('/')

    else:
        if form.validate_on_submit():
            note.title = form.title.data
            note.content = form.content.data

            db.session.commit()

            flash('Successfully edited')
            return redirect(f'/users/{note.user.username}')

        else:
            return render_template('edit_note.html', form=form)

@app.post('/users/<username>/delete')
def user_delete(username):
    """
    Verifies CSRF and deletes user and their notes from tables
    Redirects to root
    """

    form = CSRFProtectForm()

    if form.validate_on_submit():

        user = User.query.get(username)
        notes = user.notes

        # Note.query.filter_by(owner=username).delete()
        # Note.query

        for note in notes:
            db.session.delete(note)

        db.session.delete(user)
        db.session.commit()
        session.pop('username', None)
        #fall through to redirect
    return redirect('/')