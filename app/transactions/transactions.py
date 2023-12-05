import json

from flask import Blueprint, flash, render_template, request, redirect, url_for, current_app, session

from app.middlewares.authentication import is_logged_in
from app.users.forms import RegisterForm
from app.utils.mysql import SQLquery


transactions_bp = Blueprint("transactions", __name__,
                  template_folder="templates", url_prefix="/transactions")

@transactions_bp.route('/', methods=['GET', 'POST'])
@is_logged_in
def create():
    if request.method == 'POST':
        description = request.form['description']
        amount = int(request.form['money'])
        date = request.form['date']
        value = int(request.form['transtype'])
        calc_amount = [-amount, amount, amount / 2, -amount / 2][value]

        user = session['user']['username']
        friend = session['friend']

        SQLquery(
            "UPDATE friends SET balance=balance+'%d' WHERE (id1='%s' AND id2='%s') OR (id1='%s' AND id2='%s')"
            % (calc_amount, user, friend, friend, user))
        SQLquery(
            "INSERT INTO history(id1,id2,amount,description,dateAdded) VALUES ('%s','%s','%s','%s','%s')"
            % (user, friend, calc_amount, description, date))
        return redirect(url_for('dash.dashboard'))
    return render_template('transactions.html')

@transactions_bp.route('/activities', methods=['GET', 'POST'])
@is_logged_in
def activities():
    if request.method == 'POST':
        s = request.form['delete']
        # current_app.logger.debug(s.replace("'", '"'))
        # current_app.logger.debug(json.loads(s.replace("'", '"')))
        # SQLquery(
        #     "DELETE FROM history WHERE id1='%s' AND id2='%s' AND amount='%s' AND description='%s' AND dateAdded='%s'"
        #     % (s['id1'], s['id2'], int(
        #         s['amount']), s['description'], s['dateAdded']))
        return redirect(url_for('transactions.activities'))
    username = session['user']['username']
    session['data'] = SQLquery(
        "SELECT * FROM history WHERE id1='%s' or id2='%s'" %
        (username, username))
    if not session['data']:
        flash("No activities yet!", 'danger')
        return render_template('activities.html')
    for i in range(len(session['data'])):
        if session['data'][i]['id1'] == username:
            session['data'][i]['name'] = session['data'][i]['id1']
        if session['data'][i]['id2'] == username:
            session['data'][i]['name'] = session['data'][i]['id2']
    return render_template('activities.html')
