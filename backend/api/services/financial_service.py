import os
from alpha_vantage.timeseries import TimeSeries
import finnhub
import yfinance as yf
from twelvedata import TDClient
import google.generativeai as genai
from decimal import Decimal
from datetime import datetime, timedelta
from ..models import StockData, AIRecommendation, UserProfile

class FinancialService:
    def __init__(self):
        # Initialize API clients
        self.alpha_vantage = TimeSeries(key=os.getenv('ALPHA_VANTAGE_API_KEY'))
        self.finnhub_client = finnhub.Client(api_key=os.getenv('FINNHUB_API_KEY'))
        self.td_client = TDClient(apikey=os.getenv('TWELVEDATA_API_KEY'))
        
        # Initialize Gemini AI
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel('gemini-pro')

    def get_stock_data(self, symbol):
        """
        Fetch comprehensive stock data from multiple sources
        """
        try:
            # Get real-time data from Finnhub
            finnhub_quote = self.finnhub_client.quote(symbol)
            
            # Get additional data from yfinance
            yf_stock = yf.Ticker(symbol)
            info = yf_stock.info
            
            # Get technical indicators from Twelve Data
            td_rsi = self.td_client.time_series(
                symbol=symbol,
                interval="1day",
                outputsize=1,
                indicator="rsi"
            ).as_json()

            # Combine all data
            stock_data = {
                'symbol': symbol,
                'name': info.get('longName', ''),
                'current_price': Decimal(str(finnhub_quote['c'])),
                'daily_high': Decimal(str(finnhub_quote['h'])),
                'daily_low': Decimal(str(finnhub_quote['l'])),
                'volume': info.get('volume', 0),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': Decimal(str(info.get('trailingPE', 0))) if info.get('trailingPE') else None,
                'dividend_yield': Decimal(str(info.get('dividendYield', 0))) if info.get('dividendYield') else None,
                'technical_indicators': {
                    'rsi': td_rsi[0]['rsi'] if td_rsi else None,
                }
            }

            # Update or create StockData record
            StockData.objects.update_or_create(
                symbol=symbol,
                defaults=stock_data
            )

            return stock_data
        except Exception as e:
            print(f"Error fetching stock data: {str(e)}")
            return None

    def generate_ai_recommendation(self, user_profile, symbol):
        """
        Generate AI-powered investment recommendation based on user profile and stock data
        """
        try:
            # Get latest stock data
            stock = StockData.objects.get(symbol=symbol)
            
            # Prepare context for AI analysis
            context = f"""
            User Profile:
            - Risk Tolerance: {user_profile.risk_tolerance}/10
            - Investment Horizon: {user_profile.investment_horizon} years

            Stock Information:
            - Company: {stock.name} ({stock.symbol})
            - Current Price: ${stock.current_price}
            - P/E Ratio: {stock.pe_ratio}
            - Dividend Yield: {stock.dividend_yield}%
            - Technical Indicators: RSI = {stock.technical_indicators.get('rsi')}

            Based on this information, provide:
            1. Investment recommendation (Buy/Hold/Sell)
            2. Confidence score (0-100)
            3. Detailed analysis including:
               - Alignment with user's risk profile
               - Technical analysis
               - Fundamental analysis
               - Potential risks and opportunities
            """

            # Generate AI response
            response = self.model.generate_content(context)
            
            # Parse AI response and create recommendation
            # Note: In a production environment, you'd want to implement more robust parsing
            recommendation = response.text
            confidence_score = 75  # You would extract this from the AI response

            # Create AI recommendation record
            ai_rec = AIRecommendation.objects.create(
                user=user_profile.user,
                symbol=symbol,
                recommendation=recommendation,
                confidence_score=confidence_score,
                analysis_data={
                    'technical_indicators': stock.technical_indicators,
                    'market_data': {
                        'price': str(stock.current_price),
                        'pe_ratio': str(stock.pe_ratio),
                        'dividend_yield': str(stock.dividend_yield)
                    }
                }
            )

            return ai_rec
        except Exception as e:
            print(f"Error generating AI recommendation: {str(e)}")
            return None

    def get_portfolio_analysis(self, portfolio):
        """
        Analyze entire portfolio and provide recommendations
        """
        try:
            # Get user profile
            user_profile = UserProfile.objects.get(user=portfolio.user)
            
            # Analyze each investment in the portfolio
            analysis = []
            total_value = Decimal('0')
            
            for investment in portfolio.investment_set.all():
                stock_data = self.get_stock_data(investment.symbol)
                if stock_data:
                    current_value = stock_data['current_price'] * investment.shares
                    total_value += current_value
                    
                    analysis.append({
                        'symbol': investment.symbol,
                        'shares': str(investment.shares),
                        'entry_price': str(investment.entry_price),
                        'current_price': str(stock_data['current_price']),
                        'current_value': str(current_value),
                        'gain_loss': str(current_value - (investment.entry_price * investment.shares))
                    })

            # Generate portfolio-level AI analysis
            context = f"""
            Portfolio Analysis for {portfolio.name}:
            Total Value: ${total_value}
            User Risk Tolerance: {user_profile.risk_tolerance}/10
            Investment Horizon: {user_profile.investment_horizon} years

            Holdings:
            {analysis}

            Provide:
            1. Portfolio diversification analysis
            2. Risk assessment
            3. Rebalancing recommendations
            4. Suggested actions for optimization
            """

            response = self.model.generate_content(context)
            
            return {
                'portfolio_name': portfolio.name,
                'total_value': str(total_value),
                'holdings': analysis,
                'ai_analysis': response.text
            }
        except Exception as e:
            print(f"Error analyzing portfolio: {str(e)}")
            return None
