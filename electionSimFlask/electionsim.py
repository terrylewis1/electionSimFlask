from flask import Flask, render_template, url_for
app = Flask(__name__)

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


if __name__ == '__main__':
    app.run(debug = True)