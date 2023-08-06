from bytespace._interface import Interface
from bytespace.exceptions import *
import requests


class DatabaseInterface(Interface):
    """
    DatabaseInterface:
    Makes connections to the bytespace server (bytespace.network) api interfaces.

    Pass the key with DatabaseInterface initialisation.
    Use the `connect()` method to connect to the DatabaseInterface.
    """

    def __init__(self, key):
        super().__init__(key)
        self.name = "DatabaseInterface"
        self.url = self.build_url(f"{self.name}.php")

    def connect(self, username=None, password=None, verify=True):
        """
        Makes a connection to the DatabaseInterface.
        If the response is an error an appropriate exception will be raised.
        Otherwise, a login token is returned.

        Automatic verification of login token is conducted via AuthInterface.
        """
        data = {"appID": self._key}

        if username is not None:
            data["username"] = username

        if password is not None:
            data["password"] = password

        res = requests.post(self.url, data=data)

        # Checking response
        if "[SUCCESS]" not in res:
            if res.text == "No username supplied!":
                raise MissingUsernameParameterError()

            elif res.text == "No password supplied!":
                raise MissingPasswordParameterError()

            elif res.text == "Requested Application couldnt be found!":
                raise InvalidAppIDError()

            else:
                raise BaseInterfaceException()

        token = res.text.replace("[SUCCESS]", "")

        if verify:
            if AuthInterface(self._key).verify(token=token):
                return token
            else:
                raise InvalidTokenError

        return token


class AuthInterface(Interface):
    """
    This interface is used to validate a login token.
    This interface is used automatically by the DatabaseInterface,
     so you do not need to verify your tokens when fetching them in this method.
    """

    def __init__(self, key):
        super().__init__(key)
        self.name = "AuthInterface"
        self.url = self.build_url(f"{self.name}.php")

    def connect(self, token=None):

        data = {"appID": self._key}

        if token is not None:
            data["token"] = token

        res = requests.post(self.url, data=data)

        return res.text.replace("[SUCCESS] ", "")

    def verify(self, token=None):
        text = self.connect(token)

        if text == "No Token supplied!":
            raise InvalidTokenError()
        elif text == "Requested Application couldnt be found!":
            raise InvalidAppIDError()
        else:
            return True


class ApplicationInterface(Interface):
    """
    The application interface is used for getting user information from bytespace servers.
    By default, this interface get the user's unique id.
    """
    def __init__(self, key):
        super().__init__(key)
        self.name = "ApplicationInterface"
        self.head = "unique"
        self.mode = "READUNIQUE"
        self.url = self.build_url(f"{self.name}.php")

    def connect(self, token=None, head="unique", mode="READUNIQUE"):

        data = {"appID": self._key}

        if token is not None:
            data["token"] = token

        data["head"] = head
        data["mode"] = mode

        res = requests.post(self.url, data=data)

        # Checking response
        if "[SUCCESS]" not in res:
            if res.text == "No Token supplied!":
                raise InvalidTokenError()

            elif res.text == "Requested Application couldnt be found!":
                raise InvalidAppIDError()

            else:
                raise BaseInterfaceException()

        return res.text.replace("[SUCCESS]", "")

