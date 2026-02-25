from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time, random

# pip install pyperclib ctrl + c , ctrl + v
import pyperclip
import os 
from dotenv import load_dotenv

# 한줄을 복사해서 붙여넣기 : 변경되게
load_dotenv(override=True)

LOGIN_ID = os.getenv('LOGIN_ID')
LOGIN_PW = os.getenv('LOGIN_PW')

url = "https://nid.naver.com/nidlogin.login"

# selenium driver 설정
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
driver = webdriver.Chrome(options=options)
driver.get(url)

# ID 입력
id_input = driver.find_element(By.ID,"id")
pyperclip.copy(LOGIN_ID) # CTRL+C
id_input.click()
id_input.send_keys(Keys.CONTROL, 'v') # CTRL + V
time.sleep(random.uniform(1.5,3.5))

# PW 입력
pw_input = driver.find_element(By.ID,"pw")
pyperclip.copy(LOGIN_PW) # CTRL+C
pw_input.click()
pw_input.send_keys(Keys.CONTROL, 'v') # CTRL + V
time.sleep(random.uniform(1.5,3.5))

# 로그인 버튼클릭
login_btn = driver.find_element(By.ID,"log.login")
login_btn.click()
time.sleep(random.uniform(1.5,3.5))

# 블로그 글쓰기 메뉴 이동
driver.get("https://blog.naver.com/GoBlogWrite.naver")
time.sleep(random.uniform(1.5,3.5))

# data 입력 및 처리
time.sleep(10)
driver.quit()

