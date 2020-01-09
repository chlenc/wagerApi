import psycopg2

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
    if all_statuses:
        sqlReq = sqlReq + 'and status = \'registered\' '
    sqlReq = sqlReq + ' LIMIT 1'

    cursor.execute(sqlReq, {'username': username})
    records = cursor.fetchall()
    cursor.close()
    if len(records) > 0:
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
