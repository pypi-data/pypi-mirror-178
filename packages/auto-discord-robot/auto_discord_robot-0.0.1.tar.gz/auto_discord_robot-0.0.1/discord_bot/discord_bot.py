#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/11/24 下午3:54
# @Author  : Xsu
# @File    : discord_bot.py

import json,requests,random,time
from typing import List
from .local_corpus import sentences,local_headers

class Discord:

    def __init__(self,token,proxies=dict(https="https://127.0.0.1:41091",http="http://127.0.0.1:41091")):
        self.uuid = token
        self.proxies = proxies

    def sendMessage(self,raw_message, url_id):
        try:
            send_url = f'https://discord.com/api/v9/channels/{url_id}/messages'
            payload = {'content': raw_message}
            header = {
                'authorization': self.uuid,
                'connection': 'close',
                'content-type': 'application/json',
                'user-agent': random.choice(local_headers),
            }
            result = requests.post(send_url, data=json.dumps(payload), headers=header, proxies=self.proxies).text
            result_obj = json.loads(result)
            if result_obj.get('code'):
                raise ValueError(f"send error -- {result_obj.get('message')}")
        except Exception as e:
            raise ValueError(f"send error -- {e}")

    def autoInvite(self):
        pass

    def autoChat(self,url_id,local_corpus=True,corpus=None,delay=1,delay_limit=10):
        if type(delay) != int or type(delay_limit) != int:
            raise ValueError(f"set delay type error -- must be int")
        if local_corpus != True and (type(corpus) != List or len(corpus) < 1):
            raise ValueError(f"set corpus error")
        if local_corpus != True:
            total_message = list(set(corpus))
        else:
            total_message = list(set(sentences))
        random.shuffle(total_message)
        for message in total_message:
            self.sendMessage(message,url_id)
            time.sleep(random.randint(delay, delay+delay_limit)) #randow sleep time


