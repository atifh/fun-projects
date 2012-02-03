#! /usr/bin/env python
## File :@(#)parse.py
## Author : Atif Haider <mail@atifhaider>

import urllib
import requests
import simplejson as json

class ParseAPI(object):
    """A Python wrapper for Parse.com API
    """

    def __init__(self, ):
        self.base_url = 'https://www.parse.com'
        self.headers = {'Content-Type': 'application/json',
                        'Author': 'Atif Haider',
                        'Author-Quote': 'Codito ergo sum!'}

    def _make_request(self, url, payload={}, method='GET'):
        url = '%s%s' % (self.base_url, url)
        if method == 'GET':
            url = '%s?%s' % (url, urllib.urlencode(payload))
            response = requests.get(url, headers=self.headers)
        else:
            # POST request!
            json_payload = json.dumps(payload)
            response = requests.post(url, data=json_payload,\
                                         headers=self.headers)
        return response.status_code

    def job_application(self, name, email, about, urls):
        """Method to apply for a job at Parse.com
        
        Arguments:
        - `name`: Applicant full name.
        - `email`: Applicant email.
        - `about`: Description about the applicant.
        - `urls`: A list of urls related the applicant.
        """
        payload = {'name': name, 'email': email,
                   'about': about, 'urls': urls}
        return self._make_request('/jobs/apply/', payload, 'POST')


if __name__ == '__main__':
    parse_obj = ParseAPI()
    name = 'Atif Haider'
    email = 'mail@atifhaider.com'
    about = """All my life i have been a Backend Developer. The code mostly i wrote is in Lisp, Clojure, Python. System Architecture, Database Design, Rest API always excites me even in the midnight. Why Parse? Yeah, i never liked dealing with templates. I like building kickass, fast, scalable backend system and expose it as API to the rest of the world and this makes me super confident that Parse will be a good fit for me and vice versa. :)"""
    urls = ['http://atifhaider.com/', 'http://github.com/atifh',
            'http://aatif.emurse.com/', 'http://launchyard.com/',
            'http://twitter.com/aatifh', 'https://github.com/atifh/fun-projects/blob/master/parse.py']
    parse_obj.job_application(name, email, about, urls)
