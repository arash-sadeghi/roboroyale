'''  
pip install lxml
pip install beautifulsoup4
pip install request
'''

import requests
from bs4 import BeautifulSoup
import os
url = 'https://roboroyale.eu/datasets/rosbags_by_day/'

r = requests.get(url, allow_redirects=True)
target_folder="/home/users/aamjadi/hdd/rosbags/"
if not os.path.exists(target_folder):
    os.mkdir(target_folder)
if not r.ok:
    print("[-] error accessing webpage")
    exit()
soup=BeautifulSoup(r.content,'lxml')
tr_list=soup.find_all('table')[0].find_all('tr')
bags=[]
for i in tr_list:
    if '.bag' in str(i):
        bags.append(i.find_all('td')[1].find('a')['href'])

os.chdir(target_folder)
for i in bags:
    if not os.path.exists(i):
        os.system("wget "+url+i)
    else:
        print("[+] file {} exists".format(i))
    # with requests.get(url+i, allow_redirects=True) as bag_data:
    #     with open(target_folder+'//'+i,'wb') as file:
    #         file.write(bag_data)
    #         # for chunk in bag_data.iter_content(chunk_size=8192): 
    #             # If you have chunk encoded response uncomment if
    #             # and set chunk_size parameter to None.
    #             # if chunk: 
    #             # f.write(chunk)

print('[+] DONE!')
