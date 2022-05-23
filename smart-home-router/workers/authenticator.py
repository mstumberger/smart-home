###############################################################################
##
##  Copyright (C) Tavendo GmbH and/or collaborators. All rights reserved.
##
##  Redistribution and use in source and binary forms, with or without
##  modification, are permitted provided that the following conditions are met:
##
##  1. Redistributions of source code must retain the above copyright notice,
##     this list of conditions and the following disclaimer.
##
##  2. Redistributions in binary form must reproduce the above copyright notice,
##     this list of conditions and the following disclaimer in the documentation
##     and/or other materials provided with the distribution.
##
##  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
##  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
##  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
##  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
##  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
##  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
##  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
##  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
##  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
##  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
##  POSSIBILITY OF SUCH DAMAGE.
##
###############################################################################
from __future__ import unicode_literals
from twisted.internet.defer import inlineCallbacks, returnValue
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError

SERVICES = {
    "control": {"secret": "secret", "role": "service"},
    "zebra": {"secret": "zebrazebra", "role": "service"},
    "terminal_LOADING": {"secret": "zebrazebra", "role": "service"},
    "terminal_ROTOLES": {"secret": "zebrazebra", "role": "service"},
    "terminal_PRESS": {"secret": "zebrazebra", "role": "service"}
}


class AuthenticatorSession(ApplicationSession):
    @inlineCallbacks
    def onJoin(self, details):

        @inlineCallbacks
        def authenticate(realm, authid, details):
            self.log.info("WAMP-CRA dynamic authenticator invoked: realm='{}', authid='{}'".format(realm, authid))
            if authid in SERVICES:
                returnValue(SERVICES[authid])
                return
            else:
                try:
                    data = yield self.call('backend.get_user', authid)
                    print(data)
                    if data:
                        algorithm, salt, iterations, keylen, derived = data['password'].split('$')
                        returnValue({'secret': derived,
                                     'salt': salt,
                                     'iterations': int(iterations),
                                     'keylen': int(keylen),
                                     'role': data['role']})
                        return
                except ApplicationError:
                    raise ApplicationError('no_such_user', f'could not authenticate session - no such user {authid}')

        try:
            yield self.register(authenticate, u'authenticate')
            self.log.debug("WAMP-CRA dynamic authenticator registered!")
        except Exception as e:
            self.log.error("Failed to register dynamic authenticator: {0}".format(e))
