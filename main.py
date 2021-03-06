#!/usr/bin/env python
#coding=utf-8
import web
import pymongo
import model
import json
import random
import urllib2
import sys
reload(sys)
sys.setdefaultencoding('utf8')
# import logging
# import logging.config

# logging.config.fileConfig("logging.conf")
# #create logger
# logger = logging.getLogger("example")
#"application" code 
# logger.debug("debug message")
# logger.info("info message")
# logger.warn("warn message")
# logger.error("error message")
# logger.critical("critical message")


web.config.debug = False 

urls = (
	'/','index',
	'/area/(\w+)','Area',
	'/profile/(.*)','GetProfile',
	'/updatelikes','Like',
	'/top/(\w+)','Top',
	'/topbuget','TopRetrive',
	'/photo/(.*)','GetPhotos',
	'/home','home',
)

app = web.application(urls,globals())
#session = web.session.Session(app,web.session.DiskSotre('sessions'),initializer={'count':0})
render1 = web.template.render('templates',base="base1")
render = web.template.render('templates',base="base")
render2 = web.template.render('templates')

cs = {"sh":"上海",
					"xj":"新疆",
					"lmg":"内蒙古",
					"bj":"北京",
					"xz":"西藏",
					"hlj":"黑龙江",
					"tj":"天津",
					"ah":"安徽",
					"sc":"四川",
					"hn":"河南",
					"hb":"河北",
					"jl":"吉林",
					"ln":"辽宁",
					"js":"江苏",
					"sd":"山东",
					"fj":"福建",
					"gd":"广东",
					"xg":"香港",
					"tw":"台湾",
					"gx":"广西",
					"gz":"贵州",
					"yn":"云南",
					"cq":"重庆",
					"han":"海南",
					"gs":"甘肃",
					"qh":"青海",
					"nx":"宁夏",
					"hub":"湖北",
					"hun":"湖南",
					"cq":"重庆",
					"jx":"江西",
					"zj":"浙江",
					"sx":"山西",
					"shx":"陕西",
					"am":"澳门"}

class home:
	def GET(self):
		title = "MOMO"
		return render2.index(title)
class index:
	def GET(self):
		title = "MOMO"
		ip = web.ctx['ip']
		# ip = "65.172.48.18"
		req = "http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip=" + ip
		try:
			f = urllib2.urlopen(req)
		except URLError,e:
			print e
		for i in f:
			if "province" in json.loads(i):				
				chinesecity = json.loads(i)["province"]
				for key,value in cs.iteritems():
					if value.decode("utf-8") == chinesecity:
						city = key
						users = json.loads(model.getTop(city))
						for user in users:
							user['likes'] = int(user['likes'])
						ide = 0
						chinesecity = chinesecity.decode("utf-8") + " - "+ "热门".decode("utf-8")
						return render.top(users, city, chinesecity, ide)
				return render2.index(title)
			else:
				return render2.index(title)
				# else:
				# 	return render2.index(title)
		# return render2.index(title)
		
class Area:
	def GET(self,name):		
		city = format(name)
		for key,value in cs.iteritems():
			if key == city:
				chinesecity = value.decode("utf-8")
		ran = random.random()
		print ran
		users = json.loads(model.getRandomUser(city,ran))
		for user in users:
			user['likes'] = int(user['likes'])
		ide = 1
		return render.user(users,city,chinesecity,ide)
		

class Retrive:
	def GET(self):
		cursor = web.input().cursor
		req = web.input().city
		cursor = int(cursor)
		users = model.getLimitUser(req,cursor)
		return users    

class GetProfile:
	def GET(self,name):
		id = format(name)
		profile = json.loads(model.getUserProfile(id))
		title = profile[0]['momoid']
		return render1.profile(profile,title)

class Like:
	def GET(self):
		id = web.input().id
		user = model.add_likes(id)
		return json.dumps(user)
	def POST(self):
		print web.input()
		id = web.input().id
		user = model.reduce_likes(id)
		return json.dumps(user)

class Top:
	def GET(self,name):
		city = format(name)
		for key,value in cs.iteritems():
			if key == city:
				chinesecity = value.decode("utf-8") + " - "+ "热门".decode("utf-8")
		users = json.loads(model.getTop(city))
		for user in users:
			user['likes'] = int(user['likes'])
		ide = 0
		return render.top(users,city,chinesecity,ide)
class TopRetrive:
	def GET(self):
		city = web.input().city
		cursor = int(web.input().cursor)
		users = model.getTopPubu(city,cursor)
		return users
class GetPhotos:
	def GET(self,name):
		moid = format(name)
		user = model.getPhotos(moid)
		return user	
def notfound():
	title = "404"
	return web.notfound(render2.nofound(title))

app.notfound = notfound

if __name__ == "__main__":
	web.wsgi.runwsgi = lambda func,addr=None:web.wsgi.runfcgi(func,addr)
	app.run()
