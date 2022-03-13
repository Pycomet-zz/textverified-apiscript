from config import *


targetGroup = input("Input your target group invite link? ")

data_file = open(f'{cwd}/data.json')
data = json.load(data_file)

users  = [] # user that received the first messages

# import pdb; pdb.set_trace()

loop = asyncio.new_event_loop()
client = TelegramClient(StringSession(), API_ID, API_HASH, loop=loop)
client.start()
client.parse_mode = "html"

print(client.session.save())

accounts = []

# Business logic
try:
    # import pdb; pdb.set_trace()
    group_entity = client.loop.run_until_complete(
        client.get_participants(targetGroup)
    )

    # Send message amd update FROM USERS on handler
    for each in group_entity:
        users.append(each)

        client.loop.run_until_complete(
            client.send_file(each.id, "https://ibb.co/smc5jvS", caption="Hello")
        )

        # import pdb; pdb.set_trace()

        for msg in data['message']:
            if each.username != None:
                text = msg.replace("$USERNAME", each.username)
            else:
                text = msg.replace("$USERNAME", "")
            client.loop.run_until_complete(
                client.send_message(each.id, text)
            )
            client.loop.run_until_complete(
                asyncio.sleep(2)
            )

    accounts = [client.loop.run_until_complete(client.get_input_entity(user)) for user in users]

except Exception as e:
    print(e)
    print("Failed attempt! You inputed invalid data for this script.")




print("Processing Response Messages...")



# Handler to received message
@client.on(events.NewMessage(incoming=True, from_users=accounts))
async def request_handler(event):
    try:
        sender = event.user_id
        message = event.message

        if event.out == False:
            await client.send_message(sender, "Do you wish to join my Crypto Chat? ")
            
            user = await client.get_input_entity(event.user.id)
            accounts.pop(user)
        else:
            pass
        
    except AttributeError:
        pass
            

client.add_event_handler(request_handler)

# Run endlessly 
client.run_until_disconnected() 