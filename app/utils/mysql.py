from flask import current_app

mysql = current_app.config['DATABASE_CONN']

def SQLquery(s):
    cur = mysql.connection.cursor()
    res = cur.execute(s)
    if s.split()[0].lower() == 'select':
        if res:
            return cur.fetchall()
        return None
    mysql.connection.commit()
