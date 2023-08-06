import os
import requests
from requests.auth import HTTPBasicAuth

class Murasaki:
    """Murasaki instance"""

    def __init__(self, API_endpoint, language=None, timezone=None, user=None, password=None):
        if not user:
            user = os.environ.get("MURASAKI_USER")
        if not password:
            password = os.environ.get("MURASAKI_PWD")

        self._endpoint = API_endpoint
        self._language = language
        self._timezone = timezone
        self._user = user
        self._password = password

    def _call(self, engine, context, template):
        r = requests.post(
            self._endpoint.strip("/") + "/html",
            json={
                'template': template,
                'data': context,
                'engine': engine,
            },
            auth=HTTPBasicAuth(self._user, self._password)
        )
        return r.text

    def pug(self, context, template):
        return self._call("pug", context, template)

    def mustache(self, context, template):
        return self._call("mustache", context, template)

    def javascript(self, context, template):
        return self._call("javascript", context, template)

    def __str__(self):
        str = f"Murasaki: {self._endpoint}"
        if self._language:
            str += f" ({self._language})"
        return str
