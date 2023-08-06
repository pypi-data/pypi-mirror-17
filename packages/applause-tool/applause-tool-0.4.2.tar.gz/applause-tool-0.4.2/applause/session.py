import base64
import json
import os
import logging

from .errors import ConfigError
from .auth import ApplauseAuth


class AuthSession(object):
    """
    Manages user's auth session & its persistence across subsequent usages.
    """

    def __init__(self, client_id, client_secret, oauth_base_url=None, load_cookie=True):
        """
        Starts user auth session
        :param client_id:
        :param client_secret:
        :param load_cookie: If True the object will initialize itself
        :return:
        """
        self.home_dir = os.path.expanduser('~')
        self.config_path = os.path.join(self.home_dir, '.applause.json')
        self.username = ''
        self.password = ''
        self.access_token = ''

        logging.debug("Starting auth session")
        self.auth = ApplauseAuth(client_id=client_id,
                                 client_secret=client_secret,
                                 oauth_base_url=oauth_base_url)

        if load_cookie:
            self.load_cookie()

    def load_cookie(self):
        """
        Loads & initializes session instance with cookie's credentials.
        """
        logging.debug("Loading user's config: {path}".format(path=self.config_path))
        config = self._load_cookie()
        if config:
            logging.debug("Success. Authenticating through available data...")
            self.access_token = config.get('access_token')
            self.username = config.get('username')
            self.password = self._decode_password(config.get('password'))
            remember_password = bool(self.password)
            self.session = self.login(username=self.username,
                                      password=self.password,
                                      access_token=self.access_token,
                                      remember_password=remember_password)

    def get_session(self):
        return self.session

    def login(self, username=None, password=None, access_token=None, remember_password=False):
        """
        Generate & persist user auth session.
        """
        self._clean_cookie()
        session = self.auth.login(username=username, password=password, access_token=access_token)
        self._store_cookie({
            'access_token': self.auth.access_token,
            'username': username,
            'password': self._encode_password(password) if remember_password else None  # "security by obscurity". This will be solved with new AMS.
        })
        return session

    def logout(self):
        """
        Revoke active access tokens & purge cookie files from the disk.
        """
        self._clean_cookie()

    def is_active(self):
        """
        Verifies that there is an active user session available.
        """
        return self.auth.logged_in()

    def _store_cookie(self, config):
        """
        Persists user's session information in a cookie file.
        """
        with open(self.config_path, 'w') as fp:
            fp.write(json.dumps(config))

    def _load_cookie(self):
        """
        Loads user's session information from a cookie file.
        """
        if not os.path.exists(self.config_path):
            return None

        with open(self.config_path, 'r') as fp:
            config = fp.read()

        try:
            data = json.loads(config)
        except (ValueError, AttributeError) as e:
            logging.debug("Unable to read config {error}".format(error=e))
            raise ConfigError("Malformed configuration file")

        return data

    def _clean_cookie(self):
        """
        Purges user' session info from the local
        """
        if os.path.exists(self.config_path):
            os.remove(self.config_path)

    def _encode_password(self, password):
        return base64.b64encode(password) if password else None

    def _decode_password(self, encoded_password):
        if not encoded_password:
            return None

        try:
            return base64.b64decode(encoded_password)
        except TypeError:
            return None
