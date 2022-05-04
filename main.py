from flask import Flask, render_template

app = Flask(__name__)

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
 
if __name__ == "__main__":
    app.run(debug = True)