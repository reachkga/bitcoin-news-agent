import os
import json
import requests
from datetime import datetime, timezone
from dotenv import dotenv_values
from supabase import create_client
from openai import OpenAI

# Load environment variables using dotenv_values
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

def search_brave(query, sites=None, use_site_filter=True):
    """Function to search using Brave Search API"""
    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": os.getenv('BRAVE_API_KEY')
    }
    
    # Make query more specific and focused
    params = {
        "q": f"{query} in the last 24 hours",  # Changed query format
        "freshness": "pd",     # past day
        "count": 20,
        "textDecorations": "false"  # Avoid HTML markup in results
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        print(f"Search query: {params['q']}")  # Debug print
        
        if response.status_code == 200:
            data = response.json()
            if 'web' in data and 'results' in data['web']:
                print(f"Raw results count: {len(data['web']['results'])}")  # Debug print
                return data
            else:
                print("No 'web' results in response. Response structure:")
                print(json.dumps(data, indent=2)[:500])  # Print first 500 chars of response
                return None
        else:
            print(f"Error response from Brave API: {response.text}")
            return None
            
    except requests.RequestException as e:
        print(f"Error searching Brave: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def store_news_in_db(news_info, url):
    """Store news in Supabase database if URL doesn't exist"""
    try:
        # Check if URL already exists in database
        existing = supabase.table('eco_info').select('url').eq('url', url).execute()
        
        # If URL already exists, skip insertion
        if existing.data and len(existing.data) > 0:
            print("News already exists in database, skipping...")
            return None
        
        # If URL is new, insert the news
        data = {
            "finance_info": news_info,
            "url": url,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        result = supabase.table('eco_info').insert(data).execute()
        print("Successfully stored news in database")
        return result
    except Exception as e:
        print(f"Error storing data in Supabase: {e}")
        return None

def get_finance_news():
    """Main function to get finance news using OpenAI function calling"""
    
    # Define the tools/functions available to the model
    tools = [{
        "type": "function",
        "function": {
            "name": "search_brave",
            "description": "Search for latest finance news using Brave Search API",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query for finance news"
                    }
                },
                "required": ["query"],
                "additionalProperties": False
            },
            "strict": True
        }
    }]

    # Define search configurations
    searches = [
        {
            "prompt": "Search for today's stock market news, focusing on S&P 500, Dow Jones, Nasdaq, and major company earnings.",
            "use_site_filter": False
        },
        {
            "prompt": "Search for today's Bitcoin price news and major cryptocurrency market updates.",
            "use_site_filter": False
        }
    ]

    for search_config in searches:
        try:
            print(f"\nExecuting search: {search_config['prompt']}")
            
            # Get completion from OpenAI
            completion = openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": search_config['prompt']}],
                tools=tools
            )

            # Handle the model's response
            tool_calls = completion.choices[0].message.tool_calls
            if tool_calls:
                for tool_call in tool_calls:
                    if tool_call.function.name == "search_brave":
                        # Parse the arguments
                        args = json.loads(tool_call.function.arguments)
                        
                        # Execute the search
                        search_results = search_brave(
                            args["query"], 
                            use_site_filter=False
                        )
                        
                        if search_results and 'web' in search_results:
                            print(f"\nFound {len(search_results['web']['results'])} results")
                            # Process each news result
                            for result in search_results['web']['results'][:10]:  # Increased to top 10 results
                                url = result['url']
                                news_info = f"Title: {result['title']}\nDescription: {result['description']}\nSource: {url}"
                                print(f"\nProcessing news:\n{news_info}\n")
                                store_news_in_db(news_info, url)
                        else:
                            print("No results found in Brave search")
            else:
                print("No tool calls made by the model")

        except Exception as e:
            print(f"Error in get_finance_news: {e}")

if __name__ == "__main__":
    get_finance_news()
