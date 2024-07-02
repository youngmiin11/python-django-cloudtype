import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class CustomException(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__(self.message)

class Crawl:
    def __init__(self, user_id, password):
        self._session = requests.Session()
        self._id = user_id
        self._pw = password

    def _get_response(self, method, url, headers=None, body=None):
        if headers is None:
            headers = {}
        if body is None:
            body = {}
        try:
            if method == 'POST':
                response = self._session.post(url, headers=headers, data=body)
            else:
                response = self._session.get(url, headers=headers)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logger.error(f'Error in HTTP request: {str(e)}')
            raise CustomException(500, f'Error in HTTP request: {str(e)}')

    def _login(self):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        body = {'userDTO.userId': self._id, 'userDTO.password': self._pw}
        url = 'http://cyber.anyang.ac.kr/MUser.do?cmd=loginUser'
        logger.info(f"Logging in with user_id: {self._id}")
        response = self._get_response('POST', url, headers, body)

        if 'pragma' in response.headers:
            logger.error("Login Failed")
            raise CustomException(300, 'Login Failed')
        
        logger.info(f"Login successful")

    def _fetch_user_info(self):
        url = 'http://cyber.anyang.ac.kr/MMain.do?cmd=viewIndexPage'
        logger.info("Fetching user info")
        response = self._get_response('GET', url)
        
        # Ensure the correct encoding is used
        response.encoding = response.apparent_encoding
        document = BeautifulSoup(response.text, 'html.parser')

        login_btn = document.find(id='login_popup')
        element = document.select_one('.login_info > ul > li:last-child')

        if login_btn:
            logger.error("Cookie has Expired")
            raise CustomException(301, 'Cookie has Expired')

        if not element:
            logger.error("User information element not found")
            raise CustomException(500, 'User information element not found')

        user_data = element.text.strip()
        data = user_data.split(' ')
        if len(data) < 2:
            logger.error("Unexpected user data format")
            raise CustomException(500, 'Unexpected user data format')

        user = {
            'name': data[0],
            'studentId': data[1][1:-1],
        }

        logger.info(f"Crawled user data: {user}")
        return user

    def crawl_user(self):
        try:
            self._login()
            return self._fetch_user_info()
        except CustomException as e:
            if e.code == 301:
                # Cookie expired, try to re-login and fetch user info again
                logger.info("Cookie expired, trying to re-login")
                self._login()
                return self._fetch_user_info()
            else:
                raise e
