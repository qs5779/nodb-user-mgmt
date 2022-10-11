# import bcrypt
# import base64
# import hashlib
# import json
# from pathlib import Path

from nodb_user_mgmt.uibase import UserInfo


class UserInfoMgr(UserInfo):
    def __init__(self, fn, salt):
        super.__init__(fn, salt)

    def adduser(self, username, password):
        if username in self.info:
            raise ValueError(f"username '{username}' already exists!!!")
        self.info[username] = {}
        self.__setpw(username, password)

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
