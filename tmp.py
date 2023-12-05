


# @app.route('/newgroup', methods=['GET', 'POST'])
# def newgroup():
#     session['friends'] = SQLquery(
#         "SELECT name, balance, phone, id FROM users,friends WHERE (id2='%s' AND id=id1) OR (id1='%s' AND id=id2)"
#         % (session['id'], session['id']))
#     if request.method == 'POST':
#         selected_users = request.form.getlist("users")
#         if not selected_users:
#             flash("No members selected", 'danger')
#             return render_template('newgroup.html')
#         SQLquery("INSERT INTO `groups`(name, size) VALUES ('%s', '%s')" %
#                  (request.form['name'], len(selected_users) + 1))
#         gr_id = SQLquery("SELECT id FROM `groups` ORDER BY id")
#         gr_id = gr_id[-1]['id']
#         SQLquery("INSERT INTO group_data VALUES ('%s','%s')" %
#                  (session['id'], gr_id))
#         for i in selected_users:
#             SQLquery("INSERT INTO group_data VALUES ('%s','%s')" % (i, gr_id))
#         return redirect(url_for('groups'))
#     return render_template('newgroup.html')


# @app.route('/grouptransactions', methods=['GET', 'POST'])
# def grouptransactions():
#     if request.method == 'POST':
#         # create new transaction query
#         description = request.form['description']
#         amount = int(request.form['money'])
#         date = request.form['date']
#         friend = int(request.form['friend'])
#         SQLquery(
#             "INSERT INTO group_transactions(id,amount,group_id,description,dateAdded) VALUES ('%s','%s','%s','%s','%s')"
#             % (friend, amount, session['cur_group_id'], description, date))
#     tr = SQLquery("SELECT * FROM group_transactions WHERE group_id='%s'" %
#                   (session['cur_group_id']))
#     group_data = SQLquery(
#         "SELECT group_data.id, users.name FROM group_data, users WHERE group_id = '%s' and users.id = group_data.id"
#         % (session['cur_group_id']))
#     session['group_data'] = group_data
#     balance = {i['id']: 0 for i in group_data}
#     mp = {i['id']: i['name'] for i in group_data}
#     session['mp'] = mp
#     session['balance'] = balance
#     if not tr:
#         flash("no transaction", 'danger')
#     else:
#         s = 0
#         for i in tr:
#             s += i['amount'] / session['cur_group_size']
#             balance[i['id']] -= i['amount']
#         for i in balance:
#             balance[i] += s
#     return render_template('grouptransactions.html')


# @app.route('/groups', methods=['GET', 'POST'])
# def groups():
#     session['groups'] = SQLquery(
#         "SELECT group_id, size, name FROM `groups`, group_data WHERE group_data.id='%s' "
#         % (session['id']))
#     if request.method == 'POST':
#         if request.form.get('create'):
#             return redirect(url_for('newgroup'))
#         else:
#             session['cur_group_id'] = request.form['view']
#             a = SQLquery("SELECT * FROM group_data WHERE group_id='%s'" %
#                          (session['cur_group_id']))
#             session['cur_group_size'] = len(a)
#             return redirect(url_for('grouptransactions'))
#     return render_template('groups.html')



