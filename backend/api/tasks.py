from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import StockAlert, Portfolio, Investment
import yfinance as yf
from decimal import Decimal

@shared_task
def check_stock_alerts():
    """
    Check all active stock alerts and trigger notifications if conditions are met
    """
    active_alerts = StockAlert.objects.filter(is_active=True, triggered=False)
    
    for alert in active_alerts:
        try:
            ticker = yf.Ticker(alert.stock_symbol)
            current_price = Decimal(str(ticker.info.get('currentPrice', 0)))
            current_volume = ticker.info.get('volume', 0)
            
            should_trigger = False
            message = ""
            
            if alert.alert_type == 'price_above' and current_price > alert.target_value:
                should_trigger = True
                message = f"{alert.stock_symbol} price is above {alert.target_value}"
            
            elif alert.alert_type == 'price_below' and current_price < alert.target_value:
                should_trigger = True
                message = f"{alert.stock_symbol} price is below {alert.target_value}"
            
            elif alert.alert_type == 'percent_change':
                prev_close = Decimal(str(ticker.info.get('previousClose', 0)))
                if prev_close > 0:
                    change = ((current_price - prev_close) / prev_close) * 100
                    if abs(change) > alert.target_value:
                        should_trigger = True
                        message = f"{alert.stock_symbol} price changed by {change:.2f}%"
            
            elif alert.alert_type == 'volume_above' and current_volume > alert.target_value:
                should_trigger = True
                message = f"{alert.stock_symbol} volume is above {alert.target_value}"
            
            if should_trigger:
                # Send email notification
                send_mail(
                    subject=f"Stock Alert: {alert.stock_symbol}",
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[alert.notification_email],
                )
                
                # Update alert status
                alert.triggered = True
                alert.last_triggered_at = timezone.now()
                alert.save()
                
        except Exception as e:
            print(f"Error processing alert for {alert.stock_symbol}: {str(e)}")

@shared_task
def update_portfolio_values():
    """
    Update the total value of all portfolios
    """
    portfolios = Portfolio.objects.all()
    
    for portfolio in portfolios:
        try:
            total_value = Decimal('0')
            investments = Investment.objects.filter(portfolio=portfolio)
            
            for investment in investments:
                ticker = yf.Ticker(investment.stock_symbol)
                current_price = Decimal(str(ticker.info.get('currentPrice', 0)))
                value = current_price * investment.shares
                total_value += value
            
            portfolio.total_value = total_value
            portfolio.save()
            
        except Exception as e:
            print(f"Error updating portfolio {portfolio.id}: {str(e)}")

@shared_task
def generate_portfolio_report(portfolio_id):
    """
    Generate and email a portfolio performance report
    """
    try:
        portfolio = Portfolio.objects.get(id=portfolio_id)
        investments = Investment.objects.filter(portfolio=portfolio)
        
        report_lines = [
            f"Portfolio Report: {portfolio.name}",
            f"Generated on: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Total Value: ${portfolio.total_value}",
            "\nInvestments:",
        ]
        
        for investment in investments:
            ticker = yf.Ticker(investment.stock_symbol)
            current_price = Decimal(str(ticker.info.get('currentPrice', 0)))
            value = current_price * investment.shares
            gain_loss = value - (investment.purchase_price * investment.shares)
            
            report_lines.extend([
                f"\n{investment.stock_symbol}:",
                f"Shares: {investment.shares}",
                f"Current Price: ${current_price}",
                f"Total Value: ${value}",
                f"Gain/Loss: ${gain_loss}",
            ])
        
        report = "\n".join(report_lines)
        
        send_mail(
            subject=f"Portfolio Report: {portfolio.name}",
            message=report,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[portfolio.user.email],
        )
        
    except Exception as e:
        print(f"Error generating report for portfolio {portfolio_id}: {str(e)}")

@shared_task
def cleanup_old_alerts():
    """
    Clean up old triggered alerts
    """
    # Delete alerts that were triggered more than 30 days ago
    thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
    StockAlert.objects.filter(
        triggered=True,
        last_triggered_at__lt=thirty_days_ago
    ).delete()
