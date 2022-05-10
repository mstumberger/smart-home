from django.contrib.auth.hashers import BasePasswordHasher
from autobahn.wamp.auth import derive_key
from django.conf import settings


class AutobahnHash(BasePasswordHasher):
    def decode(self, encoded):
        pass

    def safe_summary(self, encoded):
        pass

    algorithm = "salted_autobahn_auth"

    def verify(self, password, encoded):
        algorithm, salt, iterations, keylen, derived = encoded.split('$')
        new_password = '$'.join([
            self.algorithm,
            salt,
            iterations,
            keylen,
            derive_key(password, salt, int(iterations), int(keylen)).decode('ascii')
        ])
        return encoded == new_password

    # def safe_summary(self, encoded):
    #     algorithm, salt, iterations, keylen, derived = encoded.split('$')
    #     return OrderedDict([
    #         (__('algorithm'), algorithm),
    #         (__('salt'), salt),
    #         (__('iterations'), iterations),
    #         (__('keylen'), keylen),
    #         (__('hash'), derived),
    #     ])

    def encode(self, password, salt):
        password = '$'.join([
            self.algorithm,
            salt,
            str(settings.ITERATIONS),
            str(settings.KEYLEN),
            derive_key(password, salt, settings.ITERATIONS, settings.KEYLEN).decode('ascii')
        ])
        return password
