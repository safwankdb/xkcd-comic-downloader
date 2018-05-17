from selenium import webdriver
from urllib.request import urlretrieve
import os
files=os.listdir('./xkcd')
print('Reading existing files...')
done=0
for file in files:
	done = max(int(file.rsplit('_')[0]),done)
print(str(done)+' comics already present. Will continue from here')
web=webdriver.Chrome()
url='https://xkcd.com'
web.get(url)
prev=web.find_element_by_xpath('/html/body/div[2]/ul[2]/li[2]/a')
noOfComics=int(prev.get_attribute('href').rsplit('/')[-2])+1
print('Total images to be downloaded: '+str(noOfComics)+' - '+str(done)+' = '+str(noOfComics-done))
web.get(url+'/'+str(done+1))
for i in range(noOfComics-done):
	name=web.find_element_by_xpath('//*[@id="ctitle"]').text
	print('Downloading '+name+'...')
	next=web.find_element_by_xpath('/html/body/div[2]/ul[1]/li[4]/a')
	sources=web.find_elements_by_xpath('//div[@id="comic"]//img')
	if len(sources)>0:
		source=sources[0].get_attribute('src')
	else:
		next.click()
		continue
	name=(str(i+1+done)+'_'+name).replace('/','\\')
	urlretrieve(source, os.path.join('./xkcd',name))
	next.click()
print("All comics downloaded. Enjoy!")
web.close()