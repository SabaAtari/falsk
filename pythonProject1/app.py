from __init__ import db,app
from flask import render_template,redirect,request, url_for
from model import User,Post,Comment,Like
from forms import RegistrationForm,LoginForm,AddPost,AddComment
from flask_login import login_user,logout_user,login_required
from flask import session
from flask import flash,jsonify


@app.route('/',methods=['GET','POST'])
def login():
    form =LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Logged in Successfully')
            session['user_id'] = user.id
            session['user_name'] = user.username
            next = request.args.get('next')
            if next == None or not next[0]=='/':
                if next == None or not next[0] == '/':
                    next = url_for('my_account')
                return redirect(url_for('my_account'))
        flash('Invalid email or password')
    return render_template('login.html',form=form)

@app.route('/account')
@login_required
def my_account():
    posts = Post.query.join(User).add_columns(Post.content, Post.id, User.username).all()
    post_data = []
    for post in posts:
        likes = Like.query.filter_by(post_id=post.id).all()
        likers = [like.user.username for like in likes]
        post_data.append({
            'content': post.content,
            'username': post.username,
            'id': post.id,
            'likes': len(likes),
            'likers': likers
        })
    return render_template("my_account.html", allposts=post_data)

@app.route('/profile')
@login_required
def my_profile():
    name=session.get('user_name')
    return render_template("my_profile.html",name=name)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out')
    return redirect(url_for('login'))



@app.route('/register',methods=['GET','POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        user=User(email=form.email.data,username=form.username.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registration')
        return redirect(url_for('login'))
    return render_template('register.html',form=form)

@app.route('/addpost',methods=['GET','POST'])
@login_required
def add_post():
    form=AddPost()
    if form.validate_on_submit():
        User_id=session.get('user_id')
        post=Post(title=form.title.data,content=form.content.data,tags=form.tags.data,user_id=User_id)
        db.session.add(post)
        db.session.commit()
        flash('Post Has Been Published')
        return redirect(url_for('show_mypost'))
    return render_template('add_post.html', form=form)

@app.route('/showpost')
@login_required
def show_mypost():
    ID=session.get('user_id')
    posts=Post.query.filter_by(user_id=ID)
    post_data=[]
    for post in posts:
        post_data.append({
            'content': post.content,
            'id': post.id
        })
    return render_template('show_mypost.html',mypost=post_data)

@app.route('/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit(id):
    post=Post.query.get_or_404(id)
    form =AddPost()
    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        post.tags=form.tags.data
        db.session.add(post)
        db.session.commit()
        flash("Post Has Been Updated!")
        return redirect(url_for("show_mypost"))
    form.title.data=post.title
    form.content.data=post.content
    form.tags.data=post.tags
    return render_template("editpost.html",form=form)

@app.route("/delete/<int:id>")
@login_required
def delete(id):
    post=Post.query.get_or_404(id)
    comments=Comment.query.filter_by(post_id=id).all()
    db.session.delete(post)
    for comment in comments:
        db.session.delete(comment)
    db.session.commit()
    flash("Post Has Been Deleted!")
    return redirect(url_for('show_mypost'))



@app.route('/comment/<int:id>',methods=['POST','GET'])
@login_required
def add_comment(id):
    form=AddComment()
    if form.validate_on_submit():
        comment=Comment(content=form.content.data,user_id=session.get('user_id'),post_id=id)
        db.session.add(comment)
        db.session.commit()
        flash("Comment Has Been Added!")
        return redirect(url_for('my_account'))
    return render_template('add_comment.html',form=form)

@app.route('/showcomment/<int:id>')
@login_required
def show_comments(id):
    comments = Comment.query.filter_by(post_id=id).all()
    comment_list = []

    for comment in comments:
        username = comment.user.username
        content = comment.content
        comment_dict = {
            'username': username,
            'content': content
        }
        comment_list.append(comment_dict)
    return render_template("show_comment.html", comments=comment_list)


@app.route('/interact/<int:id>')
def interact(id):
    post = Post.query.get(id)
    if post:
        user_id = session.get('user_id')
        # Check if the user has already liked the post
        existing_like = Like.query.filter_by(post_id=post.id, user_id=user_id).first()
        if not existing_like:
            like = Like(post_id=post.id, user_id=user_id)
            db.session.add(like)
            db.session.commit()
        return redirect(url_for('my_account'))

if __name__=='__main__':
    app.run(debug=True)
