import requests
from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import date

url = 'https://www.pttweb.cc/bbs/Lifeismoney'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
threads = soup.find_all('div', {'class': 'mt-2'})

result = pd.DataFrame()
for thread in threads:
    title_list = []
    url_list = []
    time_list = []
    main_containers = thread.find_all('div', {'class': 'e7-container'})
    for container in main_containers:
        title_raw = container.find('div', {'class': 'e7-right-top-container e7-no-outline-all-descendants'}).text.strip()
        title_processed = title_raw.split('\n')[0].strip()
        url_raw = container.find('a',{'class' : 'e7-article-default'})
        url_processed = url_raw['href']
        url_final = 'https://www.pttweb.cc' + url_processed
        title_list.append(title_processed)
        url_list.append(url_final)
    
    time_containers = thread.find_all('div', {'class' : 'e7-meta-container'})
    for container in time_containers:
        time_raw = container.find_all('span', {'class': 'text-no-wrap'})
        time_processed = time_raw[1].text.strip()
        time_list.append(time_processed)


result['title'] = title_list
result['url'] = url_list
result['time'] = time_list

def lineNotifyMessage(token, msg):

    headers = {
        "Authorization": "Bearer " + token, 
        "Content-Type" : "application/x-www-form-urlencoded"
    }

    payload = {'message': msg }
    r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
    return r.status_code


for i in range(0, len(result)):
    if 'goshare' in result['title'][i].lower(): 
        if result['time'][i] == str(date.today())[5:].replace("-","/"):
            if __name__ == "__main__":
                token = '2TS4h95MpE0UB5o3UcnZMvsUOCYnUGWAS3cn2msFAPc'
                message = '\nTitle: ' + result['title'][i] + '\n' + 'URL: ' + result['url'][i] + '\n' + 'Date: ' + result['time'][i]
                lineNotifyMessage(token, message)



