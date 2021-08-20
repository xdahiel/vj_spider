from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
import time
import csv
import re

driver_path = r'path/chromedriver.exe'
csv_file_path = r'path/rank.csv'

username = 'username'
password = 'password'

contents = []
keys = []

chrome_options = Options()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--headless')

for line in open("contents.txt"):
    temp = line.split(' ')
    contents.append(temp[0])
    keys.append(temp[1])

print('处理中')

driver = webdriver.Chrome(executable_path=driver_path, chrome_options=chrome_options)

driver.get('https://vjudge.net/')
driver.find_element_by_xpath('/html/body/nav/div/ul/li[8]/a').click()
driver.implicitly_wait(1)

driver.find_element_by_id('login-username').send_keys(username)
driver.find_element_by_id('login-password').send_keys(password)
driver.find_element_by_id('btn-login').click()
driver.implicitly_wait(1)

users = []
prob = []
penalty = []
user_dict = dict()

for i in range(0, len(contents)):

    driver.implicitly_wait(1)

    content_id = contents[i]
    key = keys[i]
    content_url = 'https://vjudge.net/contest/' + content_id + '#rank'
    driver.get(content_url)
    driver.implicitly_wait(1)

    try:
        driver.find_element_by_id('contest-login-password').send_keys(key)
        driver.implicitly_wait(1)
    except:
        pass

    soup = BeautifulSoup(driver.page_source, 'lxml')
    # print(soup)

    for page in soup.find_all('tr', attrs={'c': content_id}):
        f1 = 0
        f2 = 0
        f3 = 0
        s = ''
        usr_id = -1
        cnt = 0
        for child in page.stripped_strings:
            cnt += 1
            if cnt == 2:
                if child in user_dict:
                    usr_id = user_dict[child]
                else:
                    user_dict[child] = len(users)
                    users.append(child)
                    prob.append(0)
                    penalty.append(0)
                f1 = 1
            elif f1 == 1 and f2 == 0:
                try:
                    prob[usr_id] += int(child)
                    f2 = 1
                except:
                    continue
            elif f2 == 1 and f3 == 0:
                try:
                    penalty[usr_id] += int(child)
                    f3 = 1
                    break
                except:
                    pass


def my_swap(a, b):
    prob[a], prob[b] = prob[b], prob[a]
    penalty[a], penalty[b] = penalty[b], penalty[a]
    users[a], users[b] = users[b], users[a]


# 冒泡排序
for i in range(0, len(users) - 1):
    for j in range(0, len(users) - 1 - i):
        if prob[j] < prob[j + 1]:
            my_swap(j, j + 1)
        elif prob[j] == prob[j + 1]:
            if penalty[j] > penalty[j + 1]:
                my_swap(j, j + 1)

f = open(csv_file_path, 'w', newline='', encoding='utf8')
csv_write = csv.writer(f)
csv_write.writerow(['Rank', 'ID', 'score', 'penalty'])
for i in range(0, len(users)):
    csv_write.writerow([i + 1, users[i], prob[i], penalty[i]])
f.close()
print('生成成功')

driver.close()
driver.quit()
