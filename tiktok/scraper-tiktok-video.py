from selenium import webdriver
import time
from bs4 import BeautifulSoup
import os
import pandas as pd 
print("Open Chrome browser")
driver = webdriver.Chrome()
# the tiktok link
driver.get("https://www.tiktok.com/@ala.chebbi")

time.sleep(1)

#with open('/Bureau/safe/tiktok_data.csv', 'w') as result:
 #writer = csv.writer(result)
 #writer.writerow( ('url_videos', 'video-views') )

scroll_pause_time = 1
screen_height = driver.execute_script("return window.screen.height;")
i = 1
scroll_count=6
print("Scrolling page")
while True:
  driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
  scroll_count +=9
  i += 1
  print(scroll_count)
  time.sleep(3)  
  scroll_height = driver.execute_script("return document.body.scrollHeight;")   
  if (screen_height) * i > scroll_height or scroll_count >= 200:
     break 

soup = BeautifulSoup(driver.page_source, "html.parser")
videos = soup.find_all("div", {"class": "tiktok-yz6ijl-DivWrapper e1cg0wnj1"})

print(type(videos))
for video in videos:
    print(video.a["href"])
 
#result = pd.DataFrame([videos.get('href') for videos in soup.find_all('a')], columns = ["url_video"]) 
#result.to_csv('tiktok_data.csv')

#result.to_csv('tiktok_data.csv', index=False)
#python3 scraper-tiktok-video.py
