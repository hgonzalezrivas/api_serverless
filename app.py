from flask import Flask, request
from flask_cors import  CORS, cross_origin
import logging
from upx_sls_core.UpaxController import UpaxController
from upx_sls_core.LogController import LogController

logger = logging.getLogger()
logger.setLevel(logging.INFO)
app = Flask(__name__)
upaxController = UpaxController()
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/test/get_user', methods=['POST'])
@cross_origin()
def get_user():
    from Service.UserService import UserService
    req = upaxController.decrypt(request.data)
    logger.info(req)
    response = UserService().get_user_by_cellphone(req)
    LogController().stream('test', 'get_user', req, response.response)
    logger.info(response.response)
    return upaxController.encrypt(response.create())


if __name__ == "__main__":
    app.run()