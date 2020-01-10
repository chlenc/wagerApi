import psycopg2
from werkzeug.security import generate_password_hash

conn = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="",
    host="localhost",
)

print("Database opened successfully")


def getUserByUsername(username, all_statuses):
    cursor = conn.cursor()

    sqlReq = 'SELECT * FROM users WHERE username = %(username)s '
    if not all_statuses:
        sqlReq = sqlReq + 'and status = \'registered\' '
    sqlReq = sqlReq + ' LIMIT 1'

    cursor.execute(sqlReq, {'username': username})
    records = cursor.fetchall()
    cursor.close()
    if len(records) > 0:
        return records[0]
    else:
        return None


def getPendingUser(pendinghash):
    cursor = conn.cursor()
    sqlReq = "SELECT * FROM users WHERE pendinghash = %(pendinghash)s "
    cursor.execute(sqlReq, {'pendinghash': pendinghash})
    records = cursor.fetchall()
    cursor.close()
    if len(records) is 1:
        return records[0]
    else:
        return None


def setNewPendingUser(username, pendingHash):
    cursor = conn.cursor()

    cursor.execute(
        'INSERT INTO users(username, status, pendingHash) VALUES(%s, \'pending\', %s)',
        (username, pendingHash)
    )
    conn.commit()

    cursor.close()


def registerUser(password, pendinghash, seed):
    print(password, pendinghash, seed)
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE users SET password = %(password)s, seed = %(seed)s, status = \'registered\', pendinghash = NULL WHERE pendinghash = %(pendinghash)s;',
        {'pendinghash': pendinghash, 'password': generate_password_hash(password), 'seed': seed}
        )
    conn.commit()
    cursor.close()
