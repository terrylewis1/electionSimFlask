from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = '162d99e024e23c1faf1264d14cae51ad'

posts = [ 
    {
        'author' : 'Terry Lewis',
        'title' :   'Blog post',
        'content' : 'First post content',
        'date_posted' : 'November 20, 2018'
    }, 
    {
        'author' : 'Jane Doe',
        'title' :   'Blog post',
        'content' : 'Second post content',
        'date_posted' : 'November 17, 2018'
    }

]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts = posts)

@app.route("/about")
def about():
    return render_template('about.html', title = 'About Page')

@app.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit() :
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title= 'Register', form = form)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit() :
        return redirect(url_for('home'))
    return render_template('login.html', title= 'Register', form = form)  


if __name__ == '__main__':
    app.run(debug = True)