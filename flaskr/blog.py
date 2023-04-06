# flaskr/blog.py
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from .models import Post, User, db, Category 
from datetime import datetime

bp = Blueprint('blog', __name__)

@bp.route('/')
@login_required
def index():
    """Show all the posts, most recent first."""
    posts = Post.query.join(User).join(Category).with_entities(
        Post.id, Post.title, Post.body, Post.created, Post.author_id, User.username, Category.categoryname
    ).order_by(Post.created.desc()).all()
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """Create a new post for the current user."""
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        category_id = request.form['categoryname']
        error = None

        if not title:
            error = 'Title is required.'
        elif not category_id:  # カテゴリのエラーチェックを追加
            error = 'Category is required.'
        if error is not None:
            flash(error)
        else:
            post = Post(title=title, body=body, author=g.user, category_id=category_id, created=datetime.now())
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('blog.index'))

    categories = Category.query.all()
    return render_template('blog/create.html', categories=categories)

def get_post(id, check_author=True):
    """Get a post and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    post = Post.query.get(id)

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post.author_id != g.user.id:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    """Update a post if the current user is the author."""
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        category_id = request.form['categoryname']
        error = None

        if not title:
            error = 'Title is required.'
        elif not category_id or category_id == "":  # 空の文字列のチェックを追加
            error = 'Category is required.'
        if error is not None:
            flash(error)
        else:
            post.title = title
            post.body = body
            post.category_id = category_id
            db.session.commit()
            return redirect(url_for('blog.index'))

    categories = Category.query.all()
    return render_template('blog/update.html', post=post, categories=categories)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    post = get_post(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('blog.index'))
