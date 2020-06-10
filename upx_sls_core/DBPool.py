import cx_Oracle
import logging
import os
import json
from upx_sls_core.RemoteConfig import RemoteConfig
from bson import json_util

logger = logging.getLogger()
logger.setLevel(logging.INFO)

oracle_Types = {
    'cursor': cx_Oracle.CURSOR,
    'numeric': cx_Oracle.NUMBER,
    'string': cx_Oracle.STRING
}


class DBPool():

    def __init__(self):

        self.db_info = RemoteConfig().get_config()

        self.server = self.db_info['server']
        self.port = self.db_info['port']
        self.service = self.db_info['service']
        self.user = self.db_info['user']
        self.password = self.db_info['password']

        connection = self.user + "/" + self.password + "@" + self.server + ":" + str(self.port) + "/" + self.service
        self.conn = cx_Oracle.connect(connection)
        logger.info("Oracle DB Connection: " + str(self.conn))
        self.cursor = self.conn.cursor()

    def is_alive(self):
        self.cursor.execute("select 1 from DUAL")
        if (self.cursor.fetchall()):
            return True
        else:
            return False

    def execute(self, method, name, type=None, params=None, output=None):

        db_dto = {}
        data = []

        if (method == 'FN'):
            try:
                db_execute = self.cursor.callfunc(name, oracle_Types[type],
                                                  keywordParameters=params) if params != None else self.cursor.callfunc(
                    name, oracle_Types[type])
                if type == 'cursor':
                    columns = [field[0] for field in db_execute.description]
                    rows = db_execute.fetchall() if params != None else db_execute.fetchall()
                    data = [dict(zip(columns, row)) for row in rows]
                    for d in data:
                        for key, value in d.items():
                            if isinstance(d[key], cx_Oracle.LOB):
                                d[key] = json.loads(str(value))
                    db_dto = {
                        "hasError": False,
                        "data": json.dumps(data, default=json_util.default)
                    }
                else:
                    db_dto = {
                        "hasError": False,
                        "data": db_execute
                    }
            except Exception as e:
                db_dto = {
                    "hasError": True,
                    "data": str(e)
                }
            logger.info(db_dto)
            return db_dto
        elif method == 'SP':
            try:
                db_dto = {}
                outputList = list()
                outputCnt = 0
                for i in range(0, len(params)):
                    if params[i] == 'cursor' or params[i] == 'numeric' or params[i] == 'string':
                        params[i] = self.cursor.var(oracle_Types[params[i]])
                        outputList.append(i)
                db_execute = self.cursor.callproc(name, params)
                for i in range(0, len(db_execute)):
                    if i in outputList:
                        if isinstance(db_execute[i], cx_Oracle.Cursor):
                            columns = [field[0] for field in db_execute[i].description]
                            rows = db_execute[i].fetchall()
                            db_dto[output[outputCnt]] = [dict(zip(columns, row)) for row in rows]
                        else:
                            db_dto[output[outputCnt]] = db_execute[i]
                        outputCnt += 1
                self.conn.close()
                return {
                    'hasError': False,
                    'data': json.dumps(db_dto, default=json_util.default)
                }
            except Exception as e:
                self.conn.close()
                return {
                    'hasError': True,
                    'data': str(e)
                }
