from utils import *
import random

def get_session(session):
    file = open(f'{cwd}/data.json')
    data = json.load(file)
    sessions = data['sessions']
    
    if session != "":
        sessions.remove(session)
    # return sessions[0] #picks the last recorded
    return random.choice(sessions)

def run():
    "Start The Script"

    api_client = TelegramApi()
    session = ""

    while True:
        print("Welcome, Let's get started for the day.")
        print("""
        Here are the commands;
        - Press (1) to create a new account
        - Press (2) to send out messages and await response
        - Press (3) to exit the application
        - Press (4) to check SpamBot

        Watch the console closely, as any action would have an identifier here!
        """)

        response = input(">>")

        if response == "1":
            name = input("Input a name for this new account?")

            api_client.start
            res = api_client.create_account(name)
            session = res['session']
            api_client.stop

            print(session)
            print("Created A New Account Succcessfully 👍")


        elif response == "2":
            targetGroup = input("Input your target group invite link? ")

            session = get_session(session)

            api_client.sign_in(session)
            api_client.client.loop.run_until_complete(
                api_client.send_messages(targetGroup)
            )

            print("Waiting on response......")
            api_client.run()


        elif response == "3":
            quit()

        elif response == "4":
            session = get_session(session)

            api_client.sign_in(session)

            # api_client.add_about()

            api_client.client.loop.run_until_complete(
                api_client.text_spambot()
            )

            print("Waiting on response......")
            api_client.run()

        else:
            print("You gave a wrong input. Start all over!")




if __name__ == "__main__":
    run()