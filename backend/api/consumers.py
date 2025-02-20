import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.core.cache import cache
from .models import Portfolio, Investment
from .utils import validate_stock_symbol
import yfinance as yf
import asyncio

class StockConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.symbol = self.scope['url_route']['kwargs']['symbol']
        try:
            validate_stock_symbol(self.symbol)
            self.room_name = f"stock_{self.symbol}"
            self.room_group_name = f"stock_group_{self.symbol}"
            
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            
            # Start sending real-time updates
            asyncio.create_task(self.send_stock_updates())
            
        except Exception as e:
            await self.close()

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
        except:
            pass

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'stock_message',
                    'message': message
                }
            )
        except:
            pass

    async def stock_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def send_stock_updates(self):
        while True:
            try:
                # Get stock data
                stock_data = await self.get_stock_data(self.symbol)
                
                # Send update to WebSocket
                await self.send(text_data=json.dumps({
                    'type': 'stock_update',
                    'data': stock_data
                }))
                
                # Wait for 5 seconds before next update
                await asyncio.sleep(5)
                
            except Exception as e:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': str(e)
                }))
                break

    @database_sync_to_async
    def get_stock_data(self, symbol):
        # Try to get from cache first
        cache_key = f'stock_data_{symbol}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
            
        # If not in cache, fetch from yfinance
        stock = yf.Ticker(symbol)
        data = {
            'symbol': symbol,
            'price': stock.info.get('currentPrice'),
            'change': stock.info.get('regularMarketChange'),
            'volume': stock.info.get('regularMarketVolume'),
            'high': stock.info.get('dayHigh'),
            'low': stock.info.get('dayLow'),
        }
        
        # Cache for 60 seconds
        cache.set(cache_key, data, 60)
        return data

class PortfolioConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.portfolio_id = self.scope['url_route']['kwargs']['portfolio_id']
        self.user = self.scope['user']
        
        if not self.user.is_authenticated:
            await self.close()
            return
            
        try:
            # Verify portfolio belongs to user
            portfolio = await self.get_portfolio()
            if not portfolio:
                await self.close()
                return
                
            self.room_name = f"portfolio_{self.portfolio_id}"
            self.room_group_name = f"portfolio_group_{self.portfolio_id}"
            
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            
            # Start sending portfolio updates
            asyncio.create_task(self.send_portfolio_updates())
            
        except Exception as e:
            await self.close()

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
        except:
            pass

    @database_sync_to_async
    def get_portfolio(self):
        try:
            return Portfolio.objects.get(id=self.portfolio_id, user=self.user)
        except Portfolio.DoesNotExist:
            return None

    @database_sync_to_async
    def get_portfolio_data(self):
        portfolio = Portfolio.objects.get(id=self.portfolio_id)
        investments = Investment.objects.filter(portfolio=portfolio)
        
        total_value = 0
        investment_data = []
        
        for investment in investments:
            stock = yf.Ticker(investment.stock_symbol)
            current_price = stock.info.get('currentPrice', 0)
            value = current_price * investment.shares
            total_value += value
            
            investment_data.append({
                'symbol': investment.stock_symbol,
                'shares': investment.shares,
                'current_price': current_price,
                'value': value,
                'gain_loss': value - (investment.purchase_price * investment.shares)
            })
            
        return {
            'total_value': total_value,
            'investments': investment_data
        }

    async def send_portfolio_updates(self):
        while True:
            try:
                # Get portfolio data
                portfolio_data = await self.get_portfolio_data()
                
                # Send update to WebSocket
                await self.send(text_data=json.dumps({
                    'type': 'portfolio_update',
                    'data': portfolio_data
                }))
                
                # Wait for 5 seconds before next update
                await asyncio.sleep(5)
                
            except Exception as e:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': str(e)
                }))
                break
