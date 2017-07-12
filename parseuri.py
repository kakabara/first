import re
import urllib.request
from urllib.request import urlopen

URL_PREFICS1=r'http://'
URL_PREFICS2=r'https://'
URL_WWW='www.'
MASK_HREF=re.compile('<a.*?href=(".*?").*?>')
G_URL=''
visited_link=[]

def print_result():
	f=open('uri.txt','r')
	i=1
	line_uri=f.readline()
	print(line_uri)
	while (line_uri):
		line_uri=f.readline()
		print(line_uri)
		i+=1
	print('Count link:',i)

def get_page(url):
	res = 'error'
	try:
		f = urllib.request.urlopen(url)
		res = f.read()
	except urllib.error.HTTPError:
		res = 'error: can\'t connect'
	except urllib.error.URLError:
		res = 'error: bad url'
	return res


def exist_URI(uri):
#существоание урл в списке найденных
	f=open('uri.txt','r')
	flag=False
	line_uri=f.readline()
	line_uri=line_uri[:-1]
	while ((not flag) and line_uri):
		if (line_uri==uri):	
			flag=True
		line_uri=f.readline()
		line_uri=line_uri[:-1]
	f.close()
	return flag

def correct_URI(uri):
#принадлежит ли к домену
	if (len(uri)>=len(G_URL)):
		if (uri.find(G_URL)>-1):
			return True
		return False
	
def get_clear_URL(URL):
#Очищаем урл от всех левых знаков в начале
	URL=URL.replace(' ','')
	URL=URL.replace(URL_PREFICS1,'')
	URL=URL.replace(URL_PREFICS2,'')
	URL=URL.replace(URL_WWW,'')
	URL=URL.replace('//','')
#убираем слэш вконце если есть
	if (URL[-1]=='/'):
		URL=URL[:-1]
	return URL

def get_URI(URI):
#получение всех ссылок помеченных тегом <a>
	page=str(get_page(URI))
	page=page.replace('\\\'','"') #заменяем одинарные ковычки на двойные
	Array_A=[]
	if (page!='error: can\'t connect' and page!='error' and page!='error: bad url'):
		Array_A=MASK_HREF.findall(page)
		return Array_A
	print (page)
	return '0'

def change_uri(uri):
#Приводим все ссылки к одному виду 'http://....' или 'https://....'
	if (uri.find('http://')==-1 and uri.find('https://')==-1):
		uri='http://'+uri
	if (uri.find('//')<0 and uri[0]=='/'):
		uri=G_URL+uri
	uri.replace('\\\"','')
	return uri

def without_anchor(uri):
	#проверим ссылку на якорь вида href="current_uri#..." или href="#..."
	if (uri[0]!='#'):
		ind=uri.find('#')
		if(ind>-1):
			uri=uri[:ind]
		return uri
	return 'anchor'	

def get_URI_frm_Page(URI):
	ar_href=get_URI(URI)
	if(ar_href=='0'):
		return
	links=[]
	for href in ar_href:	
		uri=get_clear_URL(str(href).replace('"',''))
		uri=without_anchor(uri)
		if (uri!='anchor'):
			if (correct_URI(uri)):
				if (not exist_URI(uri)):
					f=open('uri.txt','a')
					f.write(uri+'\n')
					f.close()
					links.append(uri)
					#print(uri)

	for link in links:
		print(link in visited_link)
		if (link in visited_link):
			visited_link.append(link)
			get_URI_frm_Page(change_uri(link))


Input_URL=input('Сылка должна начинаться с "http://": ')
G_URL=get_clear_URL(Input_URL)
if (len(Input_URL)!=0 and (Input_URL.find('http://')>-1 or Input_URL.find('https://')>-1)):
	f=open('uri.txt','w')
	f.write(G_URL+'\n')
	f.close()
	visited_link.append(G_URL)
	get_URI_frm_Page(Input_URL)
else:
	print("Некорректный URL")

print_result()

