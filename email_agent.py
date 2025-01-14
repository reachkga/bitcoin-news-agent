import os
import json
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from datetime import datetime, timezone
from dotenv import dotenv_values
from supabase import create_client
from openai import OpenAI
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from io import BytesIO

# Load environment variables
config = dotenv_values(".env")
os.environ.update(config)

# Initialize clients
openai_client = OpenAI(
    api_key=config['OPENAI_API_KEY']
)

supabase = create_client(
    config['SUPABASE_URL'],
    config['SUPABASE_KEY']
)

def get_latest_data():
    """Fetch latest data from both tables"""
    try:
        # Get Bitcoin price data for the last 24 hours
        today = datetime.now(timezone.utc).date()
        btc_data = supabase.table('btc_price')\
            .select('*')\
            .gte('created_at', today.isoformat())\
            .order('created_at', desc=True)\
            .execute()
        
        # Get latest news (last 10 entries)
        news_data = supabase.table('eco_info')\
            .select('*')\
            .order('timestamp', desc=True)\
            .limit(10)\
            .execute()
        
        return btc_data.data, news_data.data
    except Exception as e:
        print(f"Error fetching data from Supabase: {e}")
        return None, None

def create_analysis(btc_data, news_data):
    """Use OpenAI to analyze the data and create an email content"""
    
    # Check if we have any price data
    if not btc_data:
        return None
        
    # Check if we have any new news
    has_news = bool(news_data)
    
    # Prepare the price context
    context = "Recent Bitcoin Prices:\n"
    for price in btc_data:
        context += f"- ${price['price']:,.2f} at {price['created_at']}\n"
    
    # Create different prompts based on whether we have news
    if has_news:
        context += "\nRecent Financial News:\n"
        for news in news_data:
            context += f"- {news['finance_info']}\n"
        
        system_content = """You are a professional financial and crypto analyst. Create a very concise but insightful analysis 
                        of the recent Bitcoin price movements and related financial news. Focus on key correlations 
                        between market events and price changes. Keep the analysis short, professional, and 
                        actionable. Format in a clear email structure with a subject line. End the email with 
                        'Best Regards,' on a new line."""
    else:
        system_content = """You are a professional financial analyst. Create a very brief price update email focusing only on 
                        the Bitcoin price movements. Keep it concise and professional. Format with a subject line that 
                        indicates it's a price update only. End the email with 'Best Regards,' on a new line."""
    
    # Create the prompt for OpenAI
    messages = [
        {
            "role": "system",
            "content": system_content
        },
        {
            "role": "user",
            "content": f"Based on this data, create a {'short analysis' if has_news else 'brief price update'} email:\n\n{context}"
        }
    ]
    
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )
        
        # Add signature to the email content
        email_content = response.choices[0].message.content
        
        signature = "\n\n--\nFinance Agent\nAutomated Market Analysis\n"
        signature += "Updates every 10 minutes | 24/7 monitoring\n"
        
        # Insert signature after "Best Regards" or at the end
        if "Best Regards," in email_content:
            email_content = email_content.replace("Best Regards,", "Best Regards," + signature)
        else:
            email_content += signature
            
        return email_content
        
    except Exception as e:
        print(f"Error creating analysis with OpenAI: {e}")
        return None

def create_price_graph(btc_data):
    """Create a graph of Bitcoin prices"""
    try:
        # Convert timestamps and prices into lists
        timestamps = [datetime.fromisoformat(price['created_at'].replace('Z', '+00:00')) for price in btc_data]
        prices = [price['price'] for price in btc_data]

        # Create the plot with a larger figure size
        plt.figure(figsize=(12, 6))
        plt.plot(timestamps, prices, 'b-', label='BTC Price', linewidth=2)
        
        # Format the plot
        plt.title('Bitcoin Price Trend (24 Hours)', fontsize=14)
        plt.xlabel('Time (UTC)', fontsize=12)
        plt.ylabel('Price (USD)', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(fontsize=10)
        
        # Format x-axis to show readable timestamps
        plt.gcf().autofmt_xdate()  # Angle and align the tick labels
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  # Show hours:minutes
        
        # Add price annotations at start and end
        if prices:
            plt.annotate(f'${prices[-1]:,.2f}', 
                        (timestamps[-1], prices[-1]),
                        xytext=(10, 10), textcoords='offset points')
            plt.annotate(f'${prices[0]:,.2f}',
                        (timestamps[0], prices[0]),
                        xytext=(-10, 10), textcoords='offset points',
                        horizontalalignment='right')
        
        # Adjust layout to prevent label cutoff
        plt.tight_layout()
        
        # Save plot to bytes buffer
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=300, bbox_inches='tight')
        buf.seek(0)
        plt.close()
        
        return buf.getvalue()
        
    except Exception as e:
        print(f"Error creating graph: {e}")
        return None

def send_email(content, btc_data):
    """Send email using Gmail SMTP with graph attachment"""
    try:
        # Gmail SMTP configuration
        smtp_server = "smtp.gmail.com"
        port = 465  # For SSL
        sender_email = "reachkga@gmail.com"
        receiver_email = "kg@campaignconsultants.co"
        password = os.getenv('GMAIL_APP_PASSWORD')

        # Extract subject line
        content_parts = content.split('\n', 1)
        subject = content_parts[0].replace("Subject:", "").strip()
        body = content_parts[1].strip()
        
        print("\nEmail Content:")
        print("=" * 50)
        print(f"Subject: {subject}")
        print("-" * 50)
        print(body)
        print("=" * 50)
        
        # Create the email message
        message = MIMEMultipart()
        message["From"] = f"Finance Agent <{sender_email}>"
        message["To"] = receiver_email
        message["Subject"] = subject
        
        # Add body to email
        message.attach(MIMEText(body, "plain"))
        
        # Create and attach the graph
        graph_data = create_price_graph(btc_data)
        if graph_data:
            image = MIMEImage(graph_data)
            image.add_header('Content-ID', '<btc_graph>')
            image.add_header('Content-Disposition', 'attachment', filename='btc_price_trend.png')
            message.attach(image)
        
        # Create SSL SMTP session
        print("\nSending email...")
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.send_message(message)
        
        print("\nEmail sent successfully!")
        print(f"Check your inbox (and spam folder) at {receiver_email}")
        return True
            
    except Exception as e:
        print(f"\nError sending email: {e}")
        print(f"Error type: {type(e)}")
        return False

def run_email_agent():
    """Main function to run the email agent"""
    print("Starting email agent...")
    
    # Get latest data
    btc_data, news_data = get_latest_data()
    if not btc_data or not news_data:
        print("Failed to fetch data from database")
        return
    
    # Create analysis
    print("Creating analysis...")
    email_content = create_analysis(btc_data, news_data)
    if not email_content:
        print("Failed to create analysis")
        return
    
    # Send email with graph
    print("Sending email...")
    success = send_email(email_content, btc_data)
    if success:
        print("Email agent completed successfully!")
    else:
        print("Failed to send email")

if __name__ == "__main__":
    run_email_agent()
