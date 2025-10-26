"""
メインページビュー
"""
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """メインページ"""
    return render_template('index.html')

@main_bp.route('/settings')
def settings():
    """設定ページ"""
    return render_template('settings.html')
