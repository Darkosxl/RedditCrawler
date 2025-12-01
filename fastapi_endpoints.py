from operator import sub
from fastapi import FastAPI
from crawl import subredditcrawl

app = FastAPI()


@app.get("/crawlsubreddit")
async def root(subreddit: str, num_posts: int=3):
    return subredditcrawl(subreddit, num_posts)
