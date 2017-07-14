import psycopg2
import psycopg2.extensions
from datetime import datetime

cursor=None
Connection=None
def connect_db(hostname,username,password,database):
	try:
		global Connection
		Connection=psycopg2.connect( host=hostname,user=username,password=password,dbname=database)
	except psycopg2.Error as err:
		print("Connection error: {}".format(err))
	
	global cursor
	cursor=Connection.cursor()
	cursor.execute("SET timezone='Asia/Krasnoyarsk';")
	Connection.commit()	
	cursor.execute("SET search_path = blarg,public;")
	Connection.commit()	
	query_create="""CREATE TABLE IF NOT EXISTS table_uri (parent_uri TEXT, uri TEXT, history_date TIMESTAMP);"""
	
	try:
		cursor.execute(query_create)
		Connection.commit()		
	except psycopg2.Error as err:
		print("Create error: {}".format(err))
	return
#конец коннекта

def get_history():
	try:
		print('Введите начальное число и час')
		years_start=int(input('Введите год: '))
		month_start=int(input('Введите месяц: '))
		day_start=int(input('Введите день: '))
		hour_start=int(input('Введите час: '))	
		print('Введите конечное число и час')
		years_end=int(input('Введите год: '))
		month_end=int(input('Введите месяц: '))
		day_end=int(input('Введите день: '))
		hour_end=int(input('Введите час: '))
		date_s=datetime(years_start,month_start,day_start,hour_start,0,0)
		date_e=datetime(years_end,month_end,day_end,hour_end,59,59)
		if (date_s>date_e or month_start>12 or month_end>12 or day_start>31 or day_end>31 or hour_start>23 or hour_end>23):
			print('Ощибка ввода дат')
			return
	except ValueError:
		print('Невертный формат')

	try:
		cursor.execute("SELECT * FROM table_uri WHERE history_date>%s AND history_date<=%s ORDER BY history_date;",(date_s,date_e))		
	except psycopg2.Error as err:
		print("Select error: {}".format(err))
		return
	if (cursor.rowcount>0):
		for uri in cursor:
			print ('Ссылка родитель',uri[0],'Полученная ссылка',uri[1],'Когда получена ссылка',uri[2])
	else:
		print('Нет найденных сылок')
	return
#конец получения истории

def select_uri(uri):
	try:
		cursor.execute("SELECT uri, history_date FROM table_uri WHERE parent_uri=%s ORDER BY history_date;",(uri,))		
	except psycopg2.Error as err:
		print("Select error: {}".format(err))
		return
	print('Количество найденных сылок по uri:',uri,'=',cursor.rowcount)
	for uri in cursor:
		print ('Ссылка: ',uri[0],'Была добавлена в ',uri[1])
#конец выборки по uri

def exist_uri(parent_uri,uri):
	global cursor
	cursor.execute("SELECT history_date FROM table_uri WHERE parent_uri=%s AND uri=%s ORDER BY history_date",(parent_uri,uri))
	if (cursor.rowcount==0):
		return False
	return True
#конец проверки существования

def write_uri(parent_uri,uri):	
	try:
		cursor.execute("INSERT INTO table_uri VALUES (%s,%s,%s);",(parent_uri,uri,datetime.now()))
		Connection.commit()	
	except psycopg2.Error as err:
		print("Write error: {}".format(err))
	return
#конец записи в бд

def have_uri_parent(uri):
	try:
		cursor.execute("SELECT * FROM table_uri WHERE parent_uri=%s;",(uri,))
		if (cursor.rowcount>0):
			return True
		return False
	except psycopg2.Error as err:
		print("Select error: {}".format(err))
		return False
#конец проверки ссылки на анализ
