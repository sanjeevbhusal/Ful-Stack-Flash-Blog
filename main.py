from flask import Flask, render_template, flash, redirect, url_for
from forms import RegistrationForm, LoginForm
app = Flask(__name__)


app.config["SECRET_KEY"] = '2bfaddd9ea201c72b8d450029046cc6d'
posts = [
    {
        "author": "Snajeev",
        "title": "How to be Better Developer",
        "content": "Learn EveryDay",
        "date_posted": "2022/05/05",
    }
]


@app.route("/")
def home():
    return render_template("app.html", title="Home Page", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About", body="This is an about Page")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    # only runs when form is submitted.
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@gmail.com" and form.password.data == "admin":
            flash("You are succesfullt logged In.", "success")
            return redirect(url_for("home"))
   
        else:
             flash("Please Enter correct Username or password.", "danger")
            
    return render_template("login.html", title="Login",  form=form)

if __name__ == "__main__":
    app.run(debug=True)
