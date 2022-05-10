import requests

requests.post("http://router_ip/notify",
              json={
                  'topic': 'great_topic',
                  'args': ["some, params, to, pass, along, if, you, need, to"]
})