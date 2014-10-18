import re
import os
import json
import urllib
import random
import string
import requests


def _random_string(length):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for i in range(length))


class CourseraSession(requests.Session):
    def __init__(self):
        requests.Session.__init__(self)
        self.logged_in = False


    def log_in(self, email, password):
        post_url  = 'https://accounts.coursera.org/api/v1/login'
        csrf_token, csrf2_token = _random_string(24), _random_string(24)
        csrf2_cookie = 'csrf2_token_%s' % ''.join(_random_string(8))
        params = {
            'email': email,
            'password': password,
            'webrequest': 'true'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://accounts.coursera.org',
            'Referer': 'https://accounts.coursera.org/signin',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrf_token,
            'X-CSRF2-Token': csrf2_token,
            'X-CSRF2-Cookie': csrf2_cookie,
            'Cookie': 'csrftoken=%s; %s=%s' % (csrf_token, csrf2_token, csrf2_cookie)
        }
        response = self.post(post_url, params=params, headers=headers)
        self.logged_in = response.status_code == 200
        return self.logged_in


    def download_video(self, course_id, video_id, chunk_size=1024, directory=None, callback=None):
        if not self.logged_in:
            raise Exception("Session not logged in. Log in and try again.")

        if not directory:
            directory = self.get_course_name(course_id)

        try:
            os.mkdir(directory)
        except:
            pass

        url = self.get_video_url(course_id, video_id)
        request = self.get(url, stream=True)
        file_size = int(request.headers['Content-Length'])
        file_name = re.findall(r"\"(.*)\"", request.headers['Content-Disposition'])[0]
        file_name = urllib.parse.unquote(file_name)
        file_name = re.sub('[/\\:*?"<>|]', '-', file_name)

        with open(os.path.join(directory, file_name), 'wb') as f:
            byte_count = 0
            for chunk in request.iter_content(chunk_size=chunk_size):
                f.write(chunk)
                byte_count += len(chunk)
                callback(chunk, byte_count, file_size, file_name)


    def scrape_video_ids(self, course_id):
        if not self.logged_in:
            raise Exception("Session not logged in. Log in and try again.")
        url = 'https://class.coursera.org/%s/lecture' % (course_id,)
        html = self.get(url).text
        return [int(e) for e in re.findall('mp4\?lecture_id=(.*)"', html)]


    def get_video_url(self, course_id, video_id):
        url = 'https://class.coursera.org/%s/lecture/download.mp4?lecture_id=%s'
        return url % (course_id, video_id)


    def get_course_name(self, course_id):
        c = course_id.split('-')[0]
        url = 'https://www.coursera.org/maestro/api/topic/information?topic-id=%s' % (c)
        headers = {
            'Cookie': '%s;%s' % (self.headers.setdefault('Cookie', ''), 'maestro_login_flag=1')
        }
        response = json.loads(self.get(url, headers=headers).text)
        return response['name']
