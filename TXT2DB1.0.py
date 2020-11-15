#version 1.0 - December 2019

#import packages
import re
import sqlite3
import datetime


#ask the name of the txt file
fname = input("Enter file name: ")
#ask the name of the source file - The name should be written exactly as it is in NexisUni; for instance "de Telegraaf" is correct, "Telegraaf" is not correct
Newspaper = input("Enter source name: ")

#create a database usng SQLITE - The name of the db file can be changed
conn = sqlite3.connect('Temp.sqlite')
cur = conn.cursor()

#create tables in the database usng SQLITE
cur.executescript('''
CREATE TABLE IF NOT EXISTS Articles (id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	Title TEXT,
	Newspaper TEXT,
	DatePublished TEXT,
	WeekdayPublished TEXT,
	Section TEXT,
	Length INTEGER,
	Byline TEXT,
	Subject TEXT,
	Geographic TEXT
);
CREATE TABLE IF NOT EXISTS Body (
	Body TEXT,
	Articles_id INTEGER
);
''')

# define the class of variables
n = int()
Title = str()
DatePublished = str()
WeekdayPublished = str()
Section =list()
Length = list()
Byline = list()
Subject = list()
Geographic = list()
body = int()
Body = str()

#create functions
def adjust_listlen (lstname, lstlen):
	x= lstlen - len(lstname)
	if x<0:
		del lstname[lstlen:]
	if x>0:
		for var in list(range(x)):
			lstname.append (None)

def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

def empty_list(list):
	for index, item in enumerate(list):
		list[index] = "None"

#create a dictonary for converting Duch months to English months - Can be used to make the database consistent
dutch2engmonth = {"januari":"January","februari":"February","maart":"March", "april":"April","mei":"May", "juni":"June", "juli":"July","augustus":"August","september":"September","oktober":"October","november":"November","december":"December"}

#open the file
fh = open(fname, encoding="utf8")

#read the file line by line
count = 0
body = 1
Body = ""
for line in fh:
	ly = line.rstrip()
	if ly != "":
		n=n+1
		if count == 0:
			Title = ly
			count = count + 1
			continue
		if (count == 1) and (ly != str(Newspaper)):
			Title = Title + ly
			continue
		if (count == 1) and (ly == str(Newspaper)):
			Newspaper = ly
			count = count +1
			continue
		if count == 2:
			try:
				datetime.datetime.strptime(ly, '%B %d, %Y')
				Date0 = re.split('\,', ly)
				Date1 = re.split('\s', Date0[0])
				Day = int(Date1[1])
				Year = int(Date0[1])
				Month=replace_all(Date1[0], dutch2engmonth)
				DatePublished = str(Day)+"-"+Month+"-"+str(Year)
			except ValueError:
				Date0 = re.split('\,', ly)
				try:
					datetime.datetime.strptime(Date0[0], '%B %d')
					Date1 = re.split('\s', Date0[0])
					Day = int(Date1[1])
					Month = replace_all(Date1[0], dutch2engmonth)
					Date0mid = re.split('\s', Date0[1])
					Year = int(Date0mid[1])
					DatePublished = str(Day)+"-"+Month+"-"+str(Year)
				except ValueError:
					Date1 = re.split('\s', Date0[0])
					if Date1[1]=="29" and str(Date1[0]) == ("February" or "Februari"):
						Date0mid = re.split('\s', Date0[1])
						Year = int(Date0mid[1])
						DatePublished = "29-February"+"-"+str(Year)
					else:
						Date1 = re.split('\s', ly)
						Day = int(Date1[0])
						Month = replace_all(Date1[1], dutch2engmonth)
						Year = int(Date1[2])
						DatePublished = str(Day)+"-"+Month+"-"+str(Year)
						if len(Date1) > 3:
							WeekdayPublished = Date1[3]
			count = count +1
			continue
		if (count ==3) and (ly == "End of Document"):
			count =4
		if (count ==3) and ((ly =="Body") or (body == 0)):
			if  ly != ("Classification"or "Graphic"):
				Body = Body+" "+ly
				body = 0
				continue
			else:
				body = 1
				continue
		elif (count ==3) and (ly.startswith("Section:")):
			Section = re.findall('.+\:\s(.+)\;.*',ly)
			Page = re.findall('.*\;\s([0-9]).*',ly)
			continue
		elif (count ==3) and (ly.startswith("Length:")):
			Length = re.findall('.+\:\s([0-9]*).*',ly)
			continue
		elif (count ==3) and (ly.startswith("Byline:")):
			Byline = re.findall('.+\:\s(.+)',ly)
			continue
		elif (count ==3) and (ly.startswith("Subject:")):
			Subject = re.findall('.+\:\s(.+)',ly)
			continue
		elif (count ==3) and (ly.startswith("Geographic:")):
			Geographic = re.findall('.+\:\s(.+)',ly)
			continue

		if count ==4:
			count = 0
			adjust_listlen(Section,1)
			adjust_listlen(Length,1)
			adjust_listlen(Byline,1)
			adjust_listlen(Subject,1)
			adjust_listlen(Geographic,1)

			#update the database
			cur.execute ('''INSERT INTO Articles
				(Title, Newspaper, DatePublished, WeekdayPublished, Section, Length, Byline, Subject, Geographic) VALUES (?,?,?,?,?,?,?,?,?)''', (Title, Newspaper, DatePublished, WeekdayPublished, Section[0], Length[0], Byline[0], Subject[0], Geographic[0]))
			Articles_id = cur.lastrowid
			cur.execute ('''INSERT INTO Body
				(Articles_id, Body) VALUES (?,?)''', (Articles_id, Body))
			Body = ""
			empty_list (Section)
			empty_list (Length)
			empty_list (Byline)
			empty_list (Subject)
			empty_list (Geographic)
conn.commit()
