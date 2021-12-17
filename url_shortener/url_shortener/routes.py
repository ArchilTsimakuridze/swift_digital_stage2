from flask import Blueprint, request, redirect
from .extensions import db
from .models import Link

short = Blueprint('short', __name__)

@short.route('/<short_url>')
def redirect_to_url(short_url):
    link = Link.query.filter_by(short_url=short_url).first_or_404()

    link.visits = link.visits + 1
    db.session.commit()

    return redirect(link.original_url) 

@short.route('/')
def index():
    pass

@short.route('/add_link', methods=['POST'])
def add_link():
    original_url = request.form['original_url']
    link = Link(original_url=original_url)
    db.session.add(link)
    db.session.commit()

    return link.short_url, link.original_url

@short.route('/stats')
def stats():
    links = Link.query.all()

    return links

@short.errorhandler(404)
def page_not_found(e):
    return 404