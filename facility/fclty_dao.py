import os

from pymysql import *

from pymysql import cursors


class FcltyDAO:
    def __init__(self):
        data = {}
        self.conn = connect(
            user=os.environ['DATABASE_USER'],
            password=os.environ['DATABASE_PASSWORD'],
            host=os.environ['DATABASE_HOST'],
            port=os.environ['DATABASE_PORT'],
            db=os.environ['DATABASE_NAME'],
            charset='utf8'
        )
        self.curs = self.conn.cursor(cursors.DictCursor)


    def insert_data(self, data):
        sql = "INSERT INTO facility(facility_id, facility_name, facility_telno, facility_relateurl, facility_address, facility_latitude, facility_longitude) " \
              "VALUES (%(facility_id)s, %(facility_name)s, %(facility_telno)s, %(facility_relateurl)s, %(facility_address)s, %(facility_latitude)s, %(facility_longitude)s);"
        self.curs.executemany(sql, data)
        self.conn.commit()

    def select_id_list(self):
        sql = "SELECT facility_id FROM facility"
        self.curs.execute(sql)
        list = []
        result = self.curs.fetchall()
        for data in result:
            list.append(data["facility_id"])

        return list
