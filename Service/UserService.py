import upx_sls_core.DBPool as db
import logging
import json
from Model.User import User
from upx_sls_core.Response import Response

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class UserService():

    def __init__(self):

        self.cx = db.DBPool()

    def get_user_by_cellphone(self, data):

        db_params = {
            'paCelular': data['cellphone']
        }

        user_by_cellphone = self.cx.execute('FN', 'PAUSUARIO.FNUSUARIOBYCELULAR', 'cursor', db_params)
        logger.info('User by cellphone Data: ' + str(user_by_cellphone))

        if user_by_cellphone['data']:
            for row in user_by_cellphone['data']:
                user_info = User(row['FIIDUSUARIO'], row['FCUSUARIO']).create()

            return Response('E001', True, user_info)

        else:

            return Response('ERROR', False, 'User does not exists')




