import os
import redis
from rq import Queue, Connection
from rq_scheduler import Scheduler
from datetime import datetime
from scrapers.youtube import youtube_scrape


scheduler: Scheduler = None


def init_scraper():
    global scheduler
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    conn = redis.from_url(redis_url)

    with Connection(conn):
        queue = Queue("youtube")
        scheduler = Scheduler(queue=queue)
        # You can also instantiate a Scheduler using an RQ Queue
        scheduler.schedule(
            scheduled_time=datetime.now(),  # Time for first execution, in UTC timezone
            func=youtube_scrape,  # Function to be queued
            # args=[],  # Arguments passed into function when executed
            interval=60,  # Time before the function is called again, in seconds
        )

    return scheduler


if __name__ == "__main__":
    init_scraper()
