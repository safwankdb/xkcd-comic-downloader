from selenium import webdriver
from urllib.request import urlretrieve
import os
import imghdr
folders=os.listdir('./xkcd')
if '.git'in folders:
	folders.remove('.git')
if 'README.md'in folders:
	folders.remove('README.md')
files=[]
for folder in folders:
	for file in os.listdir('./xkcd/'+folder):
		files.append(file)
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
	print('Downloading '+name+'...',end='\r')
	next=web.find_element_by_xpath('/html/body/div[2]/ul[1]/li[4]/a')
	sources=web.find_elements_by_xpath('//div[@id="comic"]//img')
	if len(sources)>0:
		source=sources[0].get_attribute('src')
	else:
		next.click()
		continue
	index=int((i+done)/1000)*1000
	if (i+1+done)%1000 == 1:
		if str(1+index)+'-'+str(index+1000) not in folders:
			os.makedirs('./xkcd/'+str(1+index)+'-'+str(index+1000))
	name=(str(i+1+done)+'_'+name).replace('/','\\')
	path=os.path.join('./xkcd/'+str(1+index)+'-'+str(index+1000)+'/',name)
	urlretrieve(source, path)
	os.rename(path,path+'.'+imghdr.what(path))
	print('Downloaded '+name)
	next.click()
print("All comics downloaded. Enjoy!")
web.close()
