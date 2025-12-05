import asyncio
from apify import Actor
from crawl import subredditcrawl, postcrawl


async def main():
    async with Actor:
        input = await Actor.get_input() or {}
        mode = input.get("mode", "subreddit")

        if mode == "subreddit":
            subreddit = input.get("subreddit", "programming")
            url = f"https://www.reddit.com/r/{subreddit}/"
            result = await subredditcrawl(url, input.get("num_posts", 10))
            for post in result.get("posts", []):
                await Actor.push_data(post)

        elif mode == "post":
            result = await postcrawl(
                input.get("post_url"),
                input.get("comment_limit", 10)
            )
            for comment in result.get("comments", []):
                await Actor.push_data(comment)


asyncio.run(main())
