

class Interface:
    """
    Base class for all interfaces.
    This class just contains some common properties/attributes used by each interface.
    This also allows you to define your own interfaces (if bytespace ever gets any new ones).
    """
    def __init__(self, key=None):
        self.domain = "bytespace.network"
        self.protocol = "https"
        self.directory = "Interfaces"

        self._key = key

    @property
    def _key(self):
        return self._key

    @_key.setter
    def _key(self, value):
        self.__key = value

    @_key.getter
    def _key(self):
        return self.__key

    def build_url(self, *args):
        url = f"{self.protocol}://{self.domain}/{self.directory}"
        for arg in args:
            url += f"/{arg}"
        return url

