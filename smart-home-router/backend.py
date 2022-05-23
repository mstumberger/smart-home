from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.types import SubscribeOptions, RegisterOptions
from datetime import datetime

version = "1.0.1"

RPC_COUNTER = {}
# List of devices
DEVICES = {'mac': None, 'sensor_id': None}

# List of uninitialized devices
uninitialized_devices = []


# List of active services, key is service name
class AppSession(ApplicationSession):
    con = None
    cur = None
    forwarder_msg_timestamp = datetime.now()
    forwarder_timestamp = datetime.now()

    SERVICES = {}
    SERVICES_SESSIONS = {}

    REGISTER_OPTIONS = RegisterOptions(details_arg='details')
    SUBSCRIBE_OPTIONS = SubscribeOptions(details_arg='details')

    MESSAGES = []

    @inlineCallbacks
    def onJoin(self, details=None):
        # DataBase connection settings
        self.log.info("Database component is connected - session ID - {}".format(details.session))
        # self.SERVICES['database'] = details.session
        # self.SERVICES_SESSIONS[details.session] = 'database'

        # Register options
        yield self.subscribe(self.on_session_join, 'wamp.session.on_join', options=self.SUBSCRIBE_OPTIONS)
        yield self.subscribe(self.on_session_leave, 'wamp.session.on_leave', options=self.SUBSCRIBE_OPTIONS)
        yield self.register(self.add_service, 'add_client', options=self.REGISTER_OPTIONS)
        yield self.register(self.online_clients, 'online_clients', options=self.REGISTER_OPTIONS)
        yield self.register(self.insert_temp, u'temp')

        print("all procedures registered")

    def on_session_join(self, session_details, details=None):
        """
        {
        u'authprovider': u'dynamic',
        u'authid': u'admin',
        u'authrole': u'anonymous',
        u'authmethod': u'wampcra',
        u'session': 8756637685336553L,
        u'authextra': None,
        u'transport': {u'cbtid': None,
        u'protocol': 'wamp.2.json',
        u'http_headers_received': {
            u'origin': u'http://localhost:3000',
            u'upgrade': u'websocket',
            u'accept-language':
            u'sl-SI,sl;q=0.9,en-GB;q=0.8,en;q=0.7',
            u'accept-encoding': u'gzip, deflate, br',
            u'sec-websocket-version': u'13',
            u'sec-websocket-protocol': u'wamp.2.json, wamp.2.msgpack',
            u'host': u'localhost:8282',
            u'sec-websocket-key': u'LFbXN//Yks+aGbFRrGK4CQ==',
            u'user-agent': u'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
            u'connection': u'Upgrade',
            u'cookie': u'csrftoken=AVmk22MV3sjwFL8UvItiisIkUxkMi7SqaZ7y21NCFZ4TuaeSy13Eb08FnHcYKmmV; sessionid=5uv29i35ug6ra0kjl41e1b04mnrv2nva',
            u'pragma': u'no-cache',
            u'cache-control': u'no-cache',
            u'sec-websocket-extensions': u'permessage-deflate;client_max_window_bits'
            },
        u'peer': u'tcp4:127.0.0.1:49662',
        u'http_headers_sent': {},
        u'websocket_extensions_in_use': [],
        u'type': 'websocket'}
        },
        """
        print(session_details, session_details['authid'])
        user = session_details['authid']
        role = session_details['authrole']
        session = int(session_details['session'])

    def on_session_leave(self, session_details, details=None):

        print("to delete", session_details)

        try:
            for client_session in self.SERVICES_SESSIONS.keys():
                self.log.info(f'Session {client_session}')
                if client_session == session_details:
                    self.log.info("Service {} with session {} was disconnected".format(
                        self.SERVICES_SESSIONS[session_details], session_details))
                    try:
                        self.SERVICES.pop(session_details, None)
                        print("self.SERVICES.pop session")
                    except KeyError:
                        print("self.SERVICES.pop session error")

                    self.publish(u'services_status', {
                        "type": "status",
                        "status": False,
                        "service": self.SERVICES_SESSIONS[session_details],
                        "data": "Service {} with session {} was disconnected".format
                        (self.SERVICES_SESSIONS[session_details], session_details)
                     })

        except Exception as e:
            self.log.error(e)

        try:
            self.SERVICES_SESSIONS.pop(session_details, None)
            print("deleted service")
        except KeyError:
            print("error service")

        self.forwarder_timestamp = datetime.now()

    def add_service(self, session, service, ip, details=None):

        self.log.info("Recieved call - add_service - : {msg} {session} - ip: {ip}",
                      msg=service, session=session, ip=ip)
        if service not in self.SERVICES:
            self.log.info("Service {} with session {} was added".format(service, session))
            self.publish(u'services_status', {
                "type": "status",
                "status": True,
                "service": service,
                "data": "Service {} with session {} was added".format(service, session)})
            self.SERVICES_SESSIONS[session] = service
            self.SERVICES[session] = {
                'available': True,
                'client': service,
                'ip': ip,
                'version': version,
                'session': session
            }
            return True
        else:
            self.log.info("Service {} already exists".format(service))
            return False

    def online_clients(self, details=None):
        self.log.info("Received call - online_services")
        return {"services": self.SERVICES, "sessions": self.SERVICES_SESSIONS}

    # def add_service(self, session, service, service_type, ip, details=None):
    #     self.log.info("Recieved call - add_service - : {msg} {session}", msg=service, session=session)
    #     if service not in self.services:
    #         self.publish(self.prefix + 'services_status', {
    #             "type": "status",
    #             "status": True,
    #             "service": service,
    #             "data": "Service {} with session {} was added".format(service, session)})
    #         self.services[service] = {'available': True, 'client': service, 'ip': ip,
    #                                   'version': version, 'type': service_type, 'session': session}
    #         self.services_sessions[session] = service
    #         print("Added service {} to list".format(service))
    #         return True
    #     else:
    #         self.log.info("Service {} already exists".format(service))
    #         return False

    def on_backend_message(self, text, type, details=None):
        print(text, type, details)
        self.MESSAGES.append(text)

    # curl -H "Content-Type: application/json" -d '{"procedure": "temp", "args": [3.4]}' http://127.0.0.1:8080/call
    @staticmethod
    def insert_temp(temp, humidity):
        print("INSERT INTO Temperatura (temp, humidity, time, date) VALUES ('%s','%s','%s','%s')" %
           (temp, humidity, datetime.datetime.now().time(), datetime.datetime.now().date()))
        return "done"
