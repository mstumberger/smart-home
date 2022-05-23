# SmarTHome Project
>## Current state
>---
>>### Server
>>- RPC function temp(temp)
    >> Saves temperature to database with current date and time
>>
>### Client for BananaPro
>>- RPC function to server (temp)
    >> Reads temperature in a loop and sends value to server
>>
>
---
# TODO
>>- Switch relay on/off
>>- Web front end
>>
>
---


1. postavi router:
   sudo apt-get update
   sudo apt-get -y install build-essential libssl-dev libffi-dev \
   libreadline-dev libbz2-dev libsqlite3-dev libncurses5-dev \
   libsnappy-dev libunwind-dev
   https://raspberrypi.stackexchange.com/questions/95143/add-apt-repository-does-not-work
   sudo add-apt-repository ppa:deadsnakes/ppa
   sudo apt update
   sudo apt install python3.9
   sudo apt install python3.9-dev
   wget https://bootstrap.pypa.io/get-pip.py
   python3.9 get-pip.py
   python3.9 -m pip install crossbar
   python3.9 -m pip install Werkzeug==2.0.3
   crossbar init
   crossbar start
    
   zaenkrat uporabi brez authentifikacije.

2. dodaj publisherja, ki posilja sporočilo, ki ga boš prejemal na topic

3. naredi create react app, ki prejema ta msg.
   https://react-redux.js.org/introduction/getting-started
   namesti node: sudo apt install nodejs
   npx create-react-app my-app --template redux-typescript
   ko imaš template spremeni store po vvzoru:
   https://github.com/mstumberger/crossbar-example-with-react/tree/master/hello-example
   https://github.com/brycedarling/redux-autobahn-js/blob/master/example/src/store.js
   https://redux.js.org/api/combinereducers
   https://blog.logrocket.com/using-typescript-with-redux-toolkit/
   https://github.com/reduxjs/redux-toolkit/issues/587
   https://stackoverflow.com/questions/64557638/how-to-polyfill-node-core-modules-in-webpack-5
   sporočilo se prikazuje
   dodaj bootstrap, https://react-bootstrap.github.io/getting-started/introduction

4. za backend:
   https://crossbar.io/docs/Adding-Real-Time-to-Django-Applications/

                        "/": {
                            "type": "wsgi",
                            "module": "smart-home-back-end-django.wsgi",
                            "object": "application"
                        },


5. relay box banana pro
   /etc/apt/sources.list
   root@192... pw bananapi
   ker se uporablja stara verzija raspbiana sem moral posodobiti mirror url
   novi mirrori http://debian.rutgers.edu/
   
   https://forums.raspberrypi.com/viewtopic.php?t=242895 zadnji post 

   instalacija python3.9
   https://itheo.tech/install-python-39-on-raspberry-pi

6. raspberry pi
   https://beebom.com/how-clone-raspberry-pi-sd-card-windows-linux-macos/
whet https://downloads.raspberrypi.org/raspios_armhf/images/raspios_armhf-2022-04-07/2022-04-04-raspios-bullseye-armhf.img.xz
tar -xf 2022-04-04-raspios-bullseye-armhf.img.xz
sudo fdisk -l
sudo umount /dev/mmcblk0p1                                                                                                                                                           927ms  pon 09 maj 2022 23:49:19
sudo umount /dev/mmcblk0p2                                                                                                                                                                       pon 09 maj 2022 23:49:43
sudo dd if=2022-04-04-raspios-bullseye-armhf.img of=/dev/mmcblk0

./manage.py collectstatic

scp smart-home-python-client/SmartHome/client/relay.py pi@192.168.88.250:/home/pi/client.py
sudo apt -y install rustc
sudo apt -y install build-essential libssl-dev libffi-dev \
python3-dev rustc cargo




GPIO interupts
https://roboticsbackend.com/raspberry-pi-gpio-interrupts-tutorial/


https://realpython.com/python-interface/
za settinge



                        "callsigned": {
                            "type": "caller",
                            "realm": "realm1",
                            "role": "anonymous",
                            "options": {
                                "key": "foobar",
                                "secret": "secret",
                                "post_body_limit": 8192,
                                "timestamp_delta_limit": 10,
                                "require_ip": [
                                    "192.168.1.1/255.255.255.0",
                                    "127.0.0.1"
                                ],
                                "require_tls": false
                            }
                        },



