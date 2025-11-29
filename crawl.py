import asyncio
import requests
from crawl4ai import LLMConfig, AsyncWebCrawler, BrowserConfig, CacheMode, CrawlerRunConfig, AdaptiveCrawler, AdaptiveConfig
import dotenv
import os


dotenv.load_dotenv()

def openrouter_embedding(query):
    response = requests.get(
      "https://openrouter.ai/api/v1/embeddings/models",
      headers={
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
      }
    )
    models = response.json()
    return models
    
    
    
 async def subredditcrawl(subreddit_url, num_posts, subject):
    async with AsyncWebCrawler() as redditcrawler:
        
        config = AdaptiveConfig(
            strategy="embedding",
            embedding_llm_config=LLMConfig(
                provider="openrouter/openai/text-embedding-3-small",
                api_token=os.getenv("OPENROUTER_API_KEY"),
                temperature=0.7
            ),
            n_query_variations=3,
            embedding_coverage_radius=0.2,
            confidence_threshold=0.8,
            max_pages=1,
            top_k_links=3,
            min_gain_threshold=0.05
        )     
        
        browser_conf = BrowserConfig(
                headless=True,
                verbose=True,
        
                # 1. THE PROXY (The Magic Key)
                proxy=PROXY_URL,
        
                # 2. SSL Fix (Equivalent to verify=False)
                ignore_https_errors=True,
        
                # 3. SAVE DATA MODE (Critical for 1GB cap)
                text_mode=True,   # Tells crawl4ai to skip loading images/media
                light_mode=True   # Disables some background listeners to save CPU
            )
        
        adaptiveredditcrawl = AdaptiveCrawler(redditcrawler, config)
        
    return 
if __name__ == "__main__":
    asyncio.run(main())
