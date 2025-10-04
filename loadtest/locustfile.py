

from locust import HttpUser, task, between
import random

class TimelineUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task(3)
    def home(self):
        user = random.randint(1, 1000)
        self.client.get(f"/timeline/home?user_id={user}&limit=30")

    @task(1)
    def post_tweet(self):
        aid = str(random.randint(1, 1000))
        self.client.post("/tweets", json={"author_id": aid, "text": "hello!"})
