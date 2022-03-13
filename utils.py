from telethon import client
from config import *

class TextVerifiedApi:

    def __init__(self) -> None:
        self.api_key = API_KEY


    def authentication(self):
        headers = {
            'X-SIMPLE-API-ACCESS-TOKEN': self.api_key
        }
        req = requests.post(
            "https://www.textverified.com/api/simpleauthentication",
            headers=headers
        ).json()
        self.access_token = req['bearer_token']
        return self.access_token

    def fetch_number(self):
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        params = {
            "id": 69 # for telegram
        }
        req = requests.post(
            "https://www.textverified.com/api/verifications",
            json=params,
            headers=headers
        )
        result = req.json()

        if isinstance(result, str) == True:
            print(f'Error - {result}')
            return False
        else:
            self.verify_id = result['id']
            return result



    def fetch_code(self):
        code = None
        while code is None:
            print("Waiting for code....")
            headers = {
                'Authorization': f'Bearer {self.access_token}'
            }
            req = requests.get(
                f"https://www.textverified.com/api/verifications/{self.verify_id}",
                headers=headers
            )
            result = req.json()
            code = result['code']
            time.sleep(5)
        return code


    def fetch_verifications(self):
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        req = requests.get(
            "https://www.textverified.com/api/verifications/pending",
            headers=headers
        )
        result = req.json()
        return result[0]


    def close_verification(self, id:str):
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        req = requests.put(
            f"https://www.textverified.com/api/verifications/{id}/report",
            headers=headers
        )
        result = req.json()
        return result


    def check_balance(self):
        pass

    def get_deposit_wallet(self):
        pass


class TelegramApi:

    def __init__(self) -> None:
        self.api_id = API_ID
        self.api_hash = API_HASH
        self.receivers = []
        self.client = None
    
    @property
    def get_proxy(self):
        proxy = {
            'proxy_type': socks.SOCKS5,
            'addr': '127.0.0.1',
            'port': 8100,
            'username': 'username',
            'password': 'password',
            'rdns': False
        }
        return proxy

    
    @property
    def start(self):
        self.loop = asyncio.new_event_loop()
        self.client = TelegramClient(StringSession(), API_ID, API_HASH, loop=self.loop)
        
        # self.client = TelegramClient(
        #     StringSession(),
        #     self.api_id,
        #     self.api_hash,
        #     connection=connection.ConnectionTcpMTProxyRandomizedIntermediate,
        #     proxy=('127.0.0.1', 3000, '00000000000000000000000000000000')
        # )

    def sign_in(self, session:str):
        "Sign In A Session ID"
        if self.client is not None:
            self.stop
        self.loop = asyncio.new_event_loop()

        # print(session)
        self.client = TelegramClient(StringSession(session), API_ID, API_HASH, loop=self.loop).start()
        print(self.client.loop.run_until_complete(self.client.get_me()))

    @property
    def session(self):
        return self.client.session.save()

    @property
    def stop(self):
        self.client.disconnect()

    def write_to_json(self, session:str):
        "Write Session to Database"
        file = open(f'{cwd}/data.json')
        data = json.load(file)

        # add session
        data['sessions'].append(session)
        with open(f'{cwd}/data.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)

    def add_about(self):
        "Add Bio & User Picture to new Account"
        # Add proxy
        # import pdb; pdb.set_trace()
        self.client.set_proxy(self.get_proxy)
        self.client.loop.run_until_complete(
            self.client(UpdateProfileRequest(
                about="Single Life Of An Enterpreneur"
            ))
        )

        group = self.client.loop.run_until_complete(
            self.client.get_entity('@teleescrowtest')
        )
        self.client.loop.run_until_complete(
            self.client(JoinChannelRequest(group))
        )

        # self.client.loop.run_until_complete(
        #     self.client(UploadProfilePhotoRequest(
        #         file=self.client.upload_file(f"{cwd}/photo.jpeg")
        #     ))
        # )

        # self.client.loop.run_until_complete(
        #     self.client(UploadProfilePhotoRequest(
        #         f"{cwd}/photo.jpeg"
        #     )
        # )

        # self.client.lo
        print(self.client.get_me())


    def create_account(self, name):
        "Verifies A New User Account"
        # fetch number
        TV_api = TextVerifiedApi()
        TV_api.authentication()
        result = TV_api.fetch_number()

        if result is False:
            pending = TV_api.fetch_verifications()
            TV_api.close_verification(pending['id'])
            result = TV_api.fetch_number()
            
        number = result['number']

        #send code
        self.client.start(
            phone=f"+1{number}",
            force_sms=True,
            code_callback=TV_api.fetch_code,
            first_name=name, # NEW ACCOUNT NAME
            last_name="Carter"
        )
        session = self.session
        self.write_to_json(session)

        self.add_about()

        return {
            "session" : session
        }


    async def send_messages(self, target:str):
        "Fetch Participants from group to an array"
        try:
            group = await self.client.get_entity(target)
            entity = await self.client.get_participants(
                    group
                )
            # self.client.loop.run_until_complete(
            #     asyncio.sleep(0.5)
            # )
            await asyncio.sleep(2)
            await self.client(JoinChannelRequest(group))

            for each in entity:
                await asyncio.sleep(2)

                user = await self.client.get_entity(each.id)
                self.receivers.append(each.id)
                
                # import pdb; pdb.set_trace()
                # await self.client.send_file(each.id, f"{cwd}/image.jpeg")
                
                
                
                for msg in data['message']:
                    if each.username != None:
                        text = msg.replace("$USERNAME", each.username)
                    else:
                        text = msg.replace("$USERNAME", "")
                    

                    await self.client.send_message(user.id, text)
                    time.sleep(2)
                    
        except Exception as e:
            print(e)
            print("Failed attempt! You inputed invalid data for this script.")
            return False

    async def text_spambot(self):
        try:
            await self.client.send_message(
                '@SpamBot',
                "/start"
            )
        except Exception as e:
            print(e)
            print("No Messaging")
    
    async def request_handler(self, event):
        try:
            sender = event.user_id
            message = event.message
            print(f"New Message Alert - {message}")

            # if event.out == False and sender in self.receivers:
            if event.out == False:
                await self.client.send_message(
                    sender,
                    "Do you wish to join my Crypto Chat?"
                )
                self.receivers.remove(sender)
            else:
                pass
        except AttributeError:
            try:
                print(event.message.message)
            except AttributeError:
                pass
        except Exception as e:
            print(e)


    def run(self):
        "Runs The Listening Handler"
        self.client.add_event_handler(self.request_handler)
        print(".....")
        self.client.run_until_disconnected()

