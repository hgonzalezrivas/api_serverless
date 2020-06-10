class Response:
    response = {}

    def __init__(self, code, success, response, message=None):
        """
        Create the response of the Method execution
        :param code (str): Response code generated
        :param success (boolean):
        :param message:
        """
        self.response = {
            'code': code,
            'success': success,
            'response': response,
            'message': message
        }

    def create(self):
        return self.response
