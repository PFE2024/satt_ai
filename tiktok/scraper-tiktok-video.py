from selenium import webdriver
import time
from bs4 import BeautifulSoup

print("Open Chrome browser")
driver = webdriver.Chrome()
# the tiktok link
driver.get("https://www.tiktok.com/@almalikaq")

time.sleep(1)

scroll_pause_time = 1
screen_height = driver.execute_script("return window.screen.height;")
i = 1

print("Scrolling page")
while True:
  driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))    
  i += 1
  time.sleep(3)
  scroll_height = driver.execute_script("return document.body.scrollHeight;")   
  if (screen_height) * i > scroll_height:
    break 

soup = BeautifulSoup(driver.page_source, "html.parser")

videos = soup.find_all("div", {"class": "tiktok-yz6ijl-DivWrapper e1cg0wnj1"})

print(len(videos))
for video in videos:
    print(video.a["href"])
  

