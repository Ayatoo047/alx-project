from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.db import connection
from django.utils.timesince import timesince
from django.shortcuts import reverse, redirect
from channels.db import database_sync_to_async
# from .models import Statistic
from base.models import Blog, Comment
from django.contrib.auth.models import User
from django_tenants.utils import schema_context
# from users.models import Profile

class RoomConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.new_message = None

    async def connect(self):
        # print(self.scope)
        url : str = self.scope['headers'][0][-1]
        url = str(url).split('.',)[0][2:]
        self.tenant = url
        room_name = self.scope['url_route']['kwargs']['slug']
        print(room_name)

        self.room_name = room_name
        # self.room_name = room_name

        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()
        print('connection')
 
   
    async def disconnect(self, close_code):
        print('disconnecting', close_code)
    

    async def receive(self, text_data):
        print('recieved')
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # extramessage = text_data_json['extramessage']
        sender = text_data_json['sender']

        # print(text_data_json['message'], sender)
        room_name = self.room_name

        # print(message)
        print('sender: ', sender)
        print('message: ', message)
        print('till here')
        await self.save_data_item(sender, message, room_name)
        print('ater here')
        self.new_message = await self.get_new()
        # self.new_messages = await self.get_new()
        # qs = await self.read_data_item(room_name)
        # new_message = self.get_new()

        await self.channel_layer.group_send(self.room_name, {
                'type' : 'statistics_message',
                'message': message,
                'sender': sender,
                # 'create': timesince(new_message['created']),
                # 'user_url': reverse("userprofile", args=[new_message['owner']])
            })

    @database_sync_to_async
    def get_new(self):
        if self.new_message is not None:
            with schema_context(self.tenant):
                new = Comment.objects.filter(id=self.new_message.id).last()
                return {'owner': new.owner_id}
        else:
            print('nothing dey')
            return {} 
        
    @database_sync_to_async
    def get_new_one(self):
        if self.new_message is not None:
            with schema_context(self.tenant):
                new = Comment.objects.filter(id=self.new_message.id).last()
                return {'owner': new.owner_id}
        else:
            print('nothing dey again')
            return {} 
        

    async def statistics_message(self, event):
        message = event['message']
        sender = event['sender']
        # print('nothing')
        # print('hhhhhh', new_message)
        # new_message = await self.get_new()
        # print(reverse("userprofile", args=[new_message['owner']]))
        # if self.new_message is None:
        #     print('if is true')
        #     self.new_message = await self.get_new_one()
        #     print("message is his: ", self.new_message)
        #     await self.send(text_data=json.dumps({
        #     'message': message,
        #     'sender': sender,
        #     # 'create': timesince(self.new_message['created']),
        #     # 'user_url': reverse("userprofile", args=[self.new_message['owner']])
        #     }))
        # else:
        try:
            created = timesince(self.new_message['created'])
            # user_url = reverse("userprofile", args=[self.new_message['owner']])
        except:
            created = 0
            user_url = 0

        # print('else is true')
        # print("message is thhhhis: ", self.new_message)
        await self.send(text_data=json.dumps({
        'message': message,
        'sender': sender,
        'create': created,
        # 'user_url': user_url
        }))
        # print(message, sender)

    @database_sync_to_async
    def create_data_item(self, sender, message, room_name):
        current_tenant : str = connection.tenant
        print(current_tenant)
        with schema_context(self.tenant):
            blogs = Blog.objects.all()
            for blog in blogs:
                print(blog.slug)
            self.new_message = Comment.objects.create(
                            owner=User.objects.filter(username=sender).first(),
                            body=message,
                            blogs=Blog.objects.filter(slug=room_name).first(),
                            )
            # print(self.new_message.__dict__)
            return self.new_message
    
    async def save_data_item(self, sender, message, room_name):
        await self.create_data_item(sender, message, room_name)
        # await self.get_new()
        
    @database_sync_to_async
    def read_data_item(self, room_name):
        with schema_context(self.tenant):    
            room = Blog.objects.filter(slug=room_name).first()
            messages = Comment.objects.filter(room=room).all()

        return messages

    # async def show_data_item(self, room_name):
    #     await self.read_data_item(room_name)