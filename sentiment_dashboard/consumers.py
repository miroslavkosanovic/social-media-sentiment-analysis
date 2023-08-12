import json
from channels.generic.websocket import AsyncWebsocketConsumer

class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def update_dashboard(self, event):
        message_type = event.get('type')
        content = event.get('content')

        await self.send(text_data=json.dumps({
            'message_type': message_type,
            'content': content,
        }))
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')

        if message_type == 'get_sentiment_data':
            # Retrieve sentiment data from the database or elsewhere
            positive_posts_count = 123
            negative_posts_count = 45
            neutral_posts_count = 78

            response_data = {
                'type': 'sentiment_data',
                'positive_posts': positive_posts_count,
                'negative_posts': negative_posts_count,
                'neutral_posts': neutral_posts_count,
            }

            # Send sentiment data response back to the client
            self.send(text_data=json.dumps(response_data))
        else:
            response_data = {
                'type': 'error',
                'message': 'Unknown message type',
            }

            # Send an error response back to the client
            self.send(text_data=json.dumps(response_data))
