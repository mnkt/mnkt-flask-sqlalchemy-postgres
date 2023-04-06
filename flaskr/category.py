from flask import Blueprint, request, render_template, flash, redirect, url_for
from flaskr.models import Category, db

category_bp = Blueprint('category', __name__, url_prefix='/category')

@category_bp.route('/', methods=['GET'])
def index():
    categories = Category.query.all()
    return render_template('category/index.html', categories=categories)

@category_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        categoryname = request.form['categoryname']
        category = Category(categoryname=categoryname)
        db.session.add(category)
        db.session.commit()
        flash('カテゴリが作成されました。')
        return redirect(url_for('category.index'))
    return render_template('category/create.html')

@category_bp.route('/<int:category_id>/edit', methods=['GET', 'POST'])
def edit(category_id):
    category = Category.query.get_or_404(category_id)
    if request.method == 'POST':
        category.categoryname = request.form['categoryname']
        db.session.commit()
        flash('カテゴリが更新されました。')
        return redirect(url_for('category.index'))
    return render_template('category/edit.html', category=category, post=category)

@category_bp.route('/<int:category_id>/delete', methods=['POST'])
def delete(category_id):
    category = Category.query.get_or_404(category_id)
    if not category.posts: # 既に記事に紐づいているカテゴリは削除できないようにする
        db.session.delete(category)
        db.session.commit()
        flash('カテゴリが削除されました。')
    else:
        flash('このカテゴリは記事に紐づいているため削除できません。')
    return redirect(url_for('category.index'))
