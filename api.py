import asyncio
import os
from lcu_driver import Connector
import json

connector = Connector()
async def check_friends(connection):
    endpoint = '/lol-chat/v1/friends'
    cwd = os.getcwd()
    file_path = cwd + '/friends_list.json'
    while True:
        friends = {}
        response = await connection.request('GET', endpoint)
        data = await response.json()
        for point in data:
            friend_name = point['name']
            friend_status = point['availability']
            if friend_status != 'mobile' and friend_status != 'offline' and friend_status != 'away':
                friends[friend_name] = friend_status

        with open(file_path, 'w') as json_file:
            json.dump(friends, json_file)
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

