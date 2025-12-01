import os
from fastapi import FastAPI, HTTPException, Header
from crawl import subredditcrawl, postcrawl
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

ENDPOINT_PASSWORD = os.getenv("ENDPOINT_PASSWORD")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/crawlpostcomments")
async def root(
    post_link:str, 
    comment_limit:int=3, 
    authorization: str=Header(None)
):
    if not authorization or authorization != f"Bearer {ENDPOINT_PASSWORD}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        data = await postcrawl(post_link, comment_limit)
        if "error" in data:
            raise HTTPException(status_code=500, detail=data["error"])

        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/crawlsubreddit")
async def root(
    subreddit: str,
    num_posts: int = 3,
    authorization: str = Header(None)
):
    if not authorization or authorization != f"Bearer {ENDPOINT_PASSWORD}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        data = await subredditcrawl(subreddit, num_posts)
        if "error" in data:
            raise HTTPException(status_code=500, detail=data["error"])

        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))