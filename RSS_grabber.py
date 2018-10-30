from subprocess import check_output
from time import gmtime, strftime, sleep
import time
import datetime
import feedparser
import configparser
import sqlite3


Delay = 60 * 60
Companies = ['AMD', 'MSFT', 'CRM', 'INTC', 'SQ']
db_file = './data/rss.db'
#Columns: time, company, title
conn = sqlite3.connect(db_file)
c = conn.cursor()
c.execute("""create table if not exists Yahoo (t text, company text, title text  PRIMARY KEY)""")
conn.commit()

try:
	while True:
		if datetime.datime.today().weekday() < 5:
			for Company in Companies:
				feed = feedparser.parse('http://finance.yahoo.com/rss/industry?s=' + Company)
				feed_entries = feed.entries
				for entry in feed.entries:
					time = strftime(entry.published, gmtime())
					title = entry.title.replace('&apos;', '\'')
					row = [time, Company, title]
					sql = '''INSERT OR IGNORE INTO Yahoo(t, company, title) VALUES(?, ?, ?)'''
					c.execute(sql, row)
					conn.commit()
		sleep(Delay)
except KeyboardInterrupt:
	conn.commit()
	c.close()