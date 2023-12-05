from flask import Blueprint, flash, render_template, request, redirect, url_for, current_app, session

from app.middlewares.authentication import is_logged_in
from app.users.forms import RegisterForm
from app.utils.mysql import SQLquery


dash_bp = Blueprint("dash", __name__,
                    template_folder="templates", url_prefix="/dash")


@dash_bp.route('/', methods=['GET', 'POST'])
@is_logged_in
def dashboard():
    if request.method == 'POST':
        if request.form.get('plus'):
            session['friend'] = request.form['plus']
            return redirect(url_for('transactions.create'))
        elif request.form.get('settle'):
            friend = request.form['settle']
            username = session['user']['username']
            SQLquery("UPDATE friends SET balance='%d' WHERE (id1='%s' AND id2='%s') OR (id1='%s' AND id2='%s')" %
                     (0, friend, username, username, friend))
            flash(f"You are now settled up with {friend}", 'success')
            return redirect(url_for('dash.dashboard'))
    username = session['user']['username']
    friends = SQLquery(
        "SELECT id1, id2, balance FROM friends WHERE id1='%s' OR id2='%s'"
        % (username, username)) or []
    friends = [{
        "name": friend['id1'] if friend['id1'] != username else friend['id2'],
        'balance': friend['balance']
    } for friend in friends]
    session['friends'] = friends
    return render_template('dashboard.html')


@dash_bp.route('/search', methods=['GET', 'POST'])
@is_logged_in
def search():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        is_client = current_app.config['IS_CLIENT']
        friend = form.name.data
        user_exists = is_client.username_exists(friend)
        if user_exists:
            cur_user = session['user']['username']
            is_friend = SQLquery(
                "SELECT * FROM friends WHERE (id1='%s' AND id2='%s') OR (id1='%s' AND id2='%s')"
                % (cur_user, friend, friend, cur_user))
            if is_friend:
                flash("You are already friends", 'danger')
            else:
                if cur_user != friend:
                    SQLquery("INSERT INTO friends VALUES ('%s','%s','%s')" %
                             (cur_user, friend, 0))
                    flash(
                        f"You are now friends with {friend}",
                        'success')
                else:
                    flash("You cannot send a request to yourself", 'danger')
            return redirect(url_for('dash.dashboard'))
        else:
            flash("This user does not exist.", 'danger')
    return render_template('search.html', form=form)
