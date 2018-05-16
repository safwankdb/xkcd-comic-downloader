from selenium import webdriver
from urllib.request import urlretrieve 
import os
files=os.listdir('./xkcd')
done=0
for file in files:
	done = max(int(file.rsplit('_')[0]),done)
web=webdriver.Chrome()
url='https://xkcd.com'
web.get(url)
prev=web.find_element_by_xpath('/html/body/div[2]/ul[2]/li[2]/a')
noOfComics=int(prev.get_attribute('href').rsplit('/')[-2])
web.get(url+'/'+str(done+1))
for i in range(noOfComics):
	name=web.find_element_by_xpath('//*[@id="ctitle"]').text
	next=web.find_element_by_xpath('/html/body/div[2]/ul[1]/li[4]/a')
	source=web.find_element_by_xpath('/html/body/div[2]/div[2]/img').get_attribute('src')
	urlretrieve(source, os.path.join('./xkcd',str(i+1+done)+'_'+name))
	next.click()
web.close()
