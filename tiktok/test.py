
from TikTokApi import TikTokApi

with TikTokApi() as api:
    user = api.user(username="therock")
    print(user.as_dict) 
      