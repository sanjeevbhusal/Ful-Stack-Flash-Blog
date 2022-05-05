from flask import Flask, render_template
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config["SECRET_KEY"] = '2bfaddd9ea201c72b8d450029046cc6d'

posts = [
    {
        "author" : "Snajeev",
        "title" : "How to be Better Developer",
        "content" : "Learn EveryDay",
        "date_posted": "2022/05/05",
    }
]

@app.route("/")
def home_page():
    return render_template("app.html", title = "Home Page", posts = posts)

@app.route("/about")
def about_page():
    return render_template("about.html", title = "About", body = "This is an about Page")

@app.route("/register")
def register():
    form = RegistrationForm()
    return render_template("register.html", title = "Register" , form = form)

@app.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html", title = "Login",  form = form)

 
if __name__ == "__main__":
    app.run(debug = True)