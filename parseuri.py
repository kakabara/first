import re
import urllib.request
import bd
from urllib.request import urlopen

URL_PREFICS1=r'http://'
URL_PREFICS2=r'https://'
URL_WWW='www.'
MASK_HREF=re.compile('<a.*?href=(".*?").*?>')
G_URL=''
visited_link=[]

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
#конец get_page


def correct_URI(uri):
#принадлежит ли к домену
	if (len(uri)>=len(G_URL)):
		if (uri.find(G_URL)>-1):
			return True
		return False
#конец correct_URI
	
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
#конец get_clear_URL

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
#конец get_URI

def change_uri(uri):
	#Приводим все ссылки к одному виду 'http://....' или 'https://....'
	if (uri.find('http://')==-1 and uri.find('https://')==-1):
		uri='http://'+uri
	if (uri.find('//')<0 and uri[0]=='/'):
		uri=G_URL+uri
	uri.replace('\\\"','')
	return uri
#конец change_URI

def without_anchor(uri):
	#проверим ссылку на якорь вида href="current_uri#..." или href="#..."
	if (uri[0]!='#'):
		ind=uri.find('#')
		if(ind>-1):
			uri=uri[:ind]
		return uri
	return 'anchor'	
#конец without_anchor

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
				if (not bd.exist_uri(G_URL,uri)):
					bd.write_uri(G_URL,uri)
					links.append(uri)
	for link in links:
		if (link in visited_link):
			visited_link.append(link)
			get_URI_frm_Page(change_uri(link))
#конец get_URI_frm_Page

def menu(option):
	print('Список команд:')
	print('0-Exit\n','1-добавление ссылок по uri\n','2-получение истории\n','3-вывести список дочерних uri\n')
	option=int(input('номер команды: '))	
	while(option!=0):
	#парсинг ссылок
		if (option==1):
			Input_URL=input('Сылка должна начинаться с "http://": ')
			global G_URL
			G_URL=get_clear_URL(Input_URL)
			if (not bd.have_uri_parent(G_URL)):
				if (len(Input_URL)!=0 and (Input_URL.find('http://')>-1 or Input_URL.find('https://')>-1)):
					get_URI_frm_Page(Input_URL)
				else:
					print('ссылка некоректна')
			else:
				print('ссылка уже была исследована')
	#посмотреть историю
		if (option==2):
			bd.get_history()
	#вывод полученных ссылок
		if(option==3):
			uri=input('Введите ссылку ')
			bd.select_uri(get_clear_URL(uri))
		if (option<0 or option>3):
			print('Список команд:')
			print('0-Exit\n','1-добавление ссылок по uri\n','2-получение истории\n','3-вывести список дочерних uri\n')
		option=int(input('номер команды:' ))	
	return
#конец меню

def start():
	print('Введите данные для подключения к бд')
	hs=input('Hostname(localhost)=')
	un=input('username=')
	ps=input('Password=')
	db_nm=input('DataBase_Name=')
	bd.connect_db(hs,un,ps,db_nm)
#конец старт




