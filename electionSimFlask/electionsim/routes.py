import secrets, os
from flask import render_template, url_for, flash, redirect, request
from electionsim import app, db, bcrypt
from electionsim.forms import RegistrationForm, LoginForm, UpdateAccountForm
from electionsim.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image

posts = [
    {
        'author': 'Terry Lewis',
        'title':   'Blog post',
        'content': 'First post content',
        'date_posted': 'November 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title':   'Blog post',
        'content': 'Second post content',
        'date_posted': 'November 17, 2018'
    }

]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About Page')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check your email and password.', 'danger')
    return render_template('login.html', title='Register', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
# Username not updating in the db.


def save_picture(form_picture) :
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_filename)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_filename

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    update_form = UpdateAccountForm()
    if update_form.validate_on_submit():
        if update_form.picture.data :
            picture_file = save_picture(update_form.picture.data)
            current_user.image_file = picture_file
        current_user.username = update_form.username.data
        current_user.email = update_form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        update_form.username.data = current_user.username
        update_form.email.data = current_user.email
    image = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image, form=update_form)
