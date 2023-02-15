import os
from sqlite3 import connect

from pymysql import *
from pickle import *

from pymysql import cursors


class PrfDAO:
    def __init__(self):
        data = {}
        with open("secret_data.pickle", "rb") as sd:
            data = load(sd)
        self.conn = connect(
            user=os.environ['DATABASE_USER'],
            password=os.environ['DATABASE_PASSWORD'],
            host=os.environ['DATABASE_HOST'],
            port=int(os.environ['DATABASE_PORT']),
            db=os.environ['DATABASE_NAME'],
            charset='utf8'
        )
        self.curs = self.conn.cursor(cursors.DictCursor)

    def insert_prf_data(self, data):
        sql = ("INSERT INTO performance(performance_id, prf_title, prf_start_date, prf_end_date, prf_cast, prf_crew, prf_runtime, prf_prd_comp, prf_viewing_age, prf_ticket_price, prf_poster, prf_story, prf_genre, prf_openrun, prf_styurls, prf_state, prf_loaded_at, facility_id) VALUES (%(performance_id)s, " +
               "%(prf_title)s, %(prf_start_date)s, " +
               "%(prf_end_date)s, %(prf_cast)s, %(prf_crew)s, %(prf_runtime)s, " +
               "%(prf_prd_comp)s, %(prf_viewing_age)s, %(prf_ticket_price)s, " +
               "%(prf_poster)s, %(prf_story)s, %(prf_genre)s, %(prf_openrun)s, " +
               "%(prf_styurls)s, %(prf_state)s, %(prf_loaded_at)s, %(facility_id)s);")
        self.curs.executemany(sql, data)
        self.conn.commit()

    def select_prf_id_list(self):
        sql = "SELECT performance_id FROM performance"
        self.curs.execute(sql)
        list = []
        result = self.curs.fetchall()
        for data in result:
            list.append(data["performance_id"])

        return list

    def insert_session_data(self, data):
        sql = (
                "INSERT INTO prf_session(performance_id, prf_session_date, prf_session_time, remaining_seat, total_seat) VALUES " +
                "(%(performance_id)s, %(prf_session_date)s, " +
                "%(prf_session_time)s, %(remaining_seat)s, %(total_seat)s);")
        self.curs.executemany(sql, data)
        self.conn.commit()