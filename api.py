import asyncio
import os
from lcu_driver import Connector
import json

connector = Connector()


async def check_friends(connection):
    endpoint_friends = '/lol-chat/v1/friends'
    endpoint_me = '/lol-chat/v1/me'
    cwd = os.getcwd()
    friend_file_path = cwd + '/friends_list.json'
    me_file_path = cwd + '/me.json'
    while True:
        friends = {}
        friend_response = await connection.request('GET', endpoint_friends)
        friend_data = await friend_response.json()

        for point in friend_data:
            friend_name = point['name']
            friend_status = point['availability']
            if friend_status != 'mobile' and friend_status != 'offline' and friend_status != 'away':
                friends[friend_name] = friend_status
        with open(friend_file_path, 'w') as json_file:
            json.dump(friends, json_file)
        json_file.close()

        me = {}
        me_response = await connection.request('GET', endpoint_me)
        me_data = await me_response.json()
        me['me'] = me_data['availability']
        with open(me_file_path, 'w') as json_file:
            json.dump(me, json_file)
        json_file.close()
        await asyncio.sleep(10)


@connector.ready
async def on_lcu_ready(connection):
    print('LCU API is ready to be used.')
    await check_friends(connection)


@connector.close
async def on_lcu_close(_):
    print('LCU API connection closed.')

connector.start()

