from fastapi import FastAPI, HTTPException
from crawl import subredditcrawl

app = FastAPI()

@app.get("/crawlsubreddit")
async def root(
    subreddit: str, 
    num_posts: int = 3
):
    try:
        data = await subredditcrawl(subreddit, num_posts, query)
        if "error" in data:
            raise HTTPException(status_code=500, detail=data["error"])
            
        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))