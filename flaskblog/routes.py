import secrets
from PIL import Image
import os
from flask import Flask, render_template, flash, redirect, url_for, request, abort
from flaskblog.forms import PostForm, RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog import app, bcrypt, db, User, Post
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
def home():
    page = request.args.get("page", 1 , type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page, per_page = 5)
    return render_template("app.html", title="Home Page", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About", body="This is an about Page")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    # only runs when form is submitted.
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Your account has been created. You are now able to log in ", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        print(user)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page =  request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        
        else:
            flash("Please Enter correct Username or password.", "danger")

    return render_template("login.html", title="Login",  form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

def save_picture(picture):
    _, file_exe = os.path.splitext(picture.filename)
    random_hex = secrets.token_hex(8)
    file_name = random_hex + file_exe
    picture_path = os.path.join(app.root_path, "static\profile_pic", file_name )
    
    output_size = (125, 125)
    i = Image.open(picture)
    i.thumbnail(output_size)    
    
    i.save(picture_path)
    
    return file_name
    
    
@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
  
    if request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
          
    elif form.validate_on_submit():
        if form.picture.data:
            file_name = save_picture(form.picture.data)
            current_user.image_file = "75ab633bfd027298.jpg"
            old_pic = current_user.image_file
            if old_pic != "default.jpg":
                os.remove(os.path.join(app.root_path, 'static/profile_pic', old_pic))
            current_user.image_file = file_name
        
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been Updated.", "success")
        return redirect(url_for("account"))
    image_file = url_for("static", filename=f"profile_pic/{current_user.image_file}")
    return render_template("account.html", title="Account", user="Sanjeev", image_file = image_file, form=form) 


@app.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("The form has been posted", "success")
        return redirect(url_for("home"))
    return render_template("create_post.html", legend = "Create Post",  title="New Post", form=form) 

@app.route("/post/<int:post_id>")
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title="Post", post=post) 
    

@app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm()
    
    if current_user.username != post.author.username:
        abort(403)
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Post Updated Succesfully.", "success")
        print(post.id)
        redirect(url_for("post", post_id = post.id ))
    
    if request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
        
    return render_template("create_post.html", title="Update Post", form=form, legend = "Update Post" ) 
    
    
@app.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash("Your post was deleted Succesfully", "success")
    return redirect(url_for("home"))
    
@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username = username).first_or_404()
    posts = Post.query.filter_by(author = user)\
            .order_by(Post.date_posted.desc())\
            .paginate(page = page, per_page = 5)
    return render_template("user_post.html", posts=posts, user=user)
