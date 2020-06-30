import psycopg2

conn2 = psycopg2.connect(dbname='tg_users', user='postgres', password='2000', host='localhost')

cur2 = conn2.cursor()


def check_user(user_id):
    cur2.execute("select * from users where user_id = " + str(user_id))
    return cur2.fetchall()


def delete_user_by_user_id(user_id):
    cur2.execute("delete from users where user_id = " + str(user_id))
    conn2.commit()


def add_user(user_id, name, surname, otchestvo, group):
    cur2.execute(
        "insert into users(user_id, name, surname, otchestvo,group_number) values (" +
        str(user_id) + ","
                       "'" + str(surname) + "',"
                                            "'" + str(name) + "',"
                                                              "'" + str(otchestvo) + "',"
                                                                                     "'" + str(group) + "')")
    conn2.commit()
