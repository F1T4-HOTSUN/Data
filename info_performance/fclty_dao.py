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
            port=int(os.environ['DATABASE_PORT']),
            db=os.environ['DATABASE_NAME'],
            charset='utf8'
        )
        try:
            self.curs = self.conn.cursor(cursors.DictCursor)
        except Exception as e:
            print("Exception occured:{}".format(e))


    def insert_data(self, data):
        try:
            sql = "INSERT INTO facility(facility_id, facility_name, facility_telno, facility_relateurl, facility_address, facility_latitude, facility_longitude) " \
                  "VALUES (%(facility_id)s, %(facility_name)s, %(facility_telno)s, %(facility_relateurl)s, %(facility_address)s, %(facility_latitude)s, %(facility_longitude)s);"
            self.curs.executemany(sql, data)
            self.conn.commit()
        except Exception as e:
            print("Exception occured:{}".format(e))
        finally:
            self.conn.close()

    def select_id_list(self):
        try:
            sql = "SELECT facility_id FROM facility"
            self.curs.execute(sql)
            list = []
            result = self.curs.fetchall()
            for data in result:
                list.append(data["facility_id"])
        except Exception as e:
            print("Exception occured:{}".format(e))
        finally:
            self.conn.close()
            return list
