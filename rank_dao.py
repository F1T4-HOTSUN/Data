import os
from sqlite3 import connect
from pymysql import *
from pymysql import cursors
from datetime import datetime, timedelta
from pytz import timezone
class RankDAO:
    def __init__(self):
        self.conn = connect(
            user=os.environ['DATABASE_USER'],
            password=os.environ['DATABASE_PASSWORD'],
            host=os.environ['DATABASE_HOST'],
            port=int(os.environ['DATABASE_PORT']),
            db=os.environ['DATABASE_NAME'],
            charset='utf8'
        )

        try:
            self.curs = self.conn.cursor(cursors.DictCursor)
        except Exception as e:
            print("Exception occured:{}".format(e))

    # def insert_rank_data(self, data):
    #     try:
    #         sql = ("INSERT INTO prf_rank(performance_id, rnum, basedate) VALUES (%(performance_id)s, %(rnum)s, %(basedate)s);")
    #         self.curs.executemany(sql, data)
    #         self.conn.commit()
    #     except Exception as e:
    #         print("Exception occured:{}".format(e))
    #     finally:
    #         self.conn.close()

    def insert_rank_data(self, data):
        try:
            sql = """
                INSERT INTO prf_rank(performance_id, rnum, basedate) 
                SELECT %(performance_id)s, %(rnum)s, %(basedate)s 
                FROM performance 
                WHERE performance_id = %(performance_id)s
            """
            self.curs.executemany(sql, data)
            self.conn.commit()
        except Exception as e:
            print("Exception occured:{}".format(e))
        finally:
            self.conn.close()

    def delete_rank_data(self):
        try:
            sql = ("DELETE FROM prf_rank WHERE basedate <= %s;")
            self.curs.execute(sql, (datetime.now(timezone('Asia/Seoul')).date() - timedelta(3)).strftime("%Y%m%d"))
            self.conn.commit()
        except Exception as e:
            print("Exception occured:{}".format(e))
        finally:
            self.conn.close()
