# import bcrypt
import base64
import hashlib
import json
from pathlib import Path


class UserInfo:
    def __init__(self, fn, salt="3WkFSpP@WBs7"):
        self.salt = salt
        self.dirty = False
        self.uipfn = Path(fn)
        self.info = {}
        if not self.uipfn.is_file():
            if self.uipfn.exists():
                import errno
                import os

                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), fn)
        else:
            with open(self.uipfn, "r") as fp:
                self.info = json.load(fp)

    def __endigest(self, password):
        # Adding salt at the last of the password
        salted = password + self.salt
        # Encoding the password
        encoded = salted.encode("utf-8")
        hashed = base64.b64encode(hashlib.sha256(encoded).digest()).decode()
        return hashed

    def __setpw(self, username, password):
        self.info[username]["pwdhash"] = self.__endigest(password)
        self.dirty = True
        self.save()

    def save(self):
        if self.dirty:
            self.show()
            with open(self.uipfn, "w") as fp:
                json.dump(self.info, fp, indent=2)
            self.dirty = False

    def checkpw(self, username, password):
        if username not in self.info:
            raise KeyError(f"username '{username}' does not exist!!!")
        hashed = self.__endigest(password)
        if hashed == self.info[username]["pwdhash"]:
            print("It Matches!")
        else:
            print("It Does not Match :(")

    def upduser(self, username, password):
        if username not in self.info:
            raise KeyError(f"username '{username}' does not exist!!!")
        self.__setpw(username, password)

    def deluser(self, username):
        if username not in self.info:
            raise KeyError(f"username '{username}' does not exist!!!")
        del self.info[username]
        self.dirty = True
        self.save()

    def show(self):
        import pprint

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.info)

    def __del__(self):
        self.save()