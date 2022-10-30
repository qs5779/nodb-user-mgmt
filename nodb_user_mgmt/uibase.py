# import bcrypt
import base64
import hashlib
import json
from pathlib import Path


class UserInfo:
    def __init__(self, src, salt, verbose=False, logger=None):
        self.logger = logger
        self.saving = False
        self.salt = salt
        self.verbose = verbose
        self.dirty = False
        try:
            self.info = json.loads(src)
        except json.JSONDecodeError:
            # if it wasn't good json then maybe it is a file
            self.uipfn = Path(src)
            if not self.uipfn.is_file():
                if self.uipfn.exists():
                    import errno
                    import os

                    raise FileNotFoundError(
                        errno.ENOENT, os.strerror(errno.ENOENT), src
                    )
                self.info = {}
            else:
                with open(self.uipfn, "r") as fp:
                    self.info = json.load(fp)
        if self.logger is not None:
            self.logger.debug(f"number of users: {len(self.info.keys())}")
            self.logger.debug(f"salt: {self.salt}")

    def __endigest(self, password):
        # Adding salt at the last of the password
        if self.logger is not None:
            self.logger.debug(f"salt: {self.salt}")
        salted = password + self.salt
        # Encoding the password
        encoded = salted.encode("utf-8")
        hashed = base64.b64encode(hashlib.sha256(encoded).digest()).decode()
        return hashed

    def _setpw(self, username, password):
        self.info[username]["pwdhash"] = self.__endigest(password)
        self.dirty = True
        self.save()

    def save(self):
        if self.dirty:
            self.saving = True
            if self.verbose:
                self.show()
            with open(self.uipfn, "w") as fp:
                json.dump(self.info, fp, indent=2)
            self.dirty = False
            self.saving = False

    def checkpw(self, username, password):
        if username not in self.info:
            raise KeyError(f"username '{username}' does not exist!!!")
        hashed = self.__endigest(password)
        match = "It Matches!"
        nomatch = "It Does not Match :("
        if hashed == self.info[username]["pwdhash"]:
            if self.verbose:
                print(match)
            return True
        if self.verbose:
            print(nomatch)
        if self.logger is not None:
            self.logger.debug(f"username: {username} password: {password}")
            self.logger.debug(nomatch)
        return False

    def show(self):
        import pprint

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.info)

    def __del__(self):
        if not self.saving:  # avoid extra exception
            self.save()
