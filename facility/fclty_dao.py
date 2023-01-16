from pymysql import *
from pickle import *


class FcltyDAO:
    def __init__(self):
        data = {}
        with open("secret_data.pickle", "rb") as sd:
            data = load(sd)
        self.conn = connect(
            user=data["database"].get("user"),
            password=data["database"].get("password"),
            host=data["database"].get("host"),
            port=data["database"].get("port"),
            db=data["database"].get("db"),
            charset='utf8'
        )
        self.curs = self.conn.cursor(cursors.DictCursor)

    def insert_data(self, data):
        sql = "INSERT INTO facility VALUES (%(facility_id)s, %(facility_name)s, %(facility_telno)s, %(facility_relateurl)s, %(facility_address)s, %(facility_latitude)s, %(facility_longitude)s);"
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
