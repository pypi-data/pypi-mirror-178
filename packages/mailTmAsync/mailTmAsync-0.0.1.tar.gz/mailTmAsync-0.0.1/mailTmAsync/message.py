import json
import time
import aiohttp


class Listen:
    listen = False
    message_ids = []
    interval = 3

    async def message_list(self, session):
        url = "https://api.mail.tm/messages"
        # headers = { 'Authorization': 'Bearer ' + self.token }
        # response = self.session.get(url, headers=headers)
        data = await self.get_json_get(session, url, proxy=None)
        # response.raise_for_status()
        # print('data: ', data)
        # data = response.json()
        return  [
                    msg for i, msg in enumerate(data['hydra:member']) 
                        if data['hydra:member'][i]['id'] not in self.message_ids
                ]

    async def message(self, session, idx):
        url = "https://api.mail.tm/messages/" + idx
        # headers = { 'Authorization': 'Bearer ' + self.token }
        # response = self.session.get(url, headers=headers)
        return await self.get_json_get(session, url, proxy=None)


    async def start_listening(self, ):
        self.listen = True
        async with aiohttp.ClientSession(headers={ 'Authorization': 'Bearer ' + self.token }) as session:
            for message in await self.message_list(session):
                self.message_ids.append(message['id'])
            id_last = self.message_ids[-1] if self.message_ids else 0
            while self.listen:
                for message in await self.message_list(session):
                    # print('msg', message['id'])
                    if message['id'] != 0 and message['id'] != id_last: 
                        new_message = await self.message(session, message['id'])
                        self.listen = False   
                time.sleep(self.interval)
        return new_message
    
    
    
    async def get_json_post(self,client: aiohttp.ClientSession, url: str,data, proxy) -> dict:
        data = json.dumps(data) if data != None else None
        if proxy == None: 
            async with client.request('post', url, data = data, ssl=False) as response:
                try: 
                    response.raise_for_status()
                except aiohttp.client_exceptions.ClientResponseError:
                    print(response)
                    return 'ClientResponseError'
                return await response.json(content_type=None)
        else: 
            async with client.request('post', url, data = data,proxy=proxy[0], proxy_auth=proxy[1], ssl=False) as response:
                try: 
                    response.raise_for_status()
                except aiohttp.client_exceptions.ClientResponseError:
                    print(response)
                    return 'ClientResponseError'
                return await response.json(content_type=None)


    async def get_json_get(self,client: aiohttp.ClientSession, url: str,proxy) -> dict:
        if proxy == None: 
            async with client.request('GET', url,ssl=False,timeout=30) as response:
                response.raise_for_status()
                return await response.json(content_type=None)
        else: 
            async with client.request('GET', url,proxy=proxy[0], proxy_auth=proxy[1],ssl=False,timeout=30) as response:
                response.raise_for_status()
                return await response.json(content_type=None)
        


