#coding=utf-8
import web
import pymongo
import model
import json



urls = (
	'/','index',
	'/area/(\w+)','Area',
	'/pbget','Retrive',
	'/profile/(.*)','GetProfile',
	'/updatelikes','Like',
)

app = web.application(urls,globals())

#session = web.session.Session(app,web.session.DiskSotre('sessions'),initializer={'count':0})
render1 = web.template.render('templates',base="base1")
render = web.template.render('templates',base="base")

class index:
	def GET(self):
		title = "MOMO"
		return render.index(title)
		
class Area:
	def GET(self,name):
		cs = {"sh":"上海",
					"xj":"新疆",
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
		ceil = lambda x:int(x) + 1
		city = format(name)
		for key,value in cs.iteritems():
			if key == city:
				chinesecity = value.decode("utf-8")
		counts = model.getCount(city)#get the user counts in some city
		last = ceil(counts/400)
		if web.input():
			page = web.input().page
			if page != last:
				cursor = (int(page)-1)*300 + 1
				users = json.loads(model.getLimitUser(city,cursor))
			else:
				cursor = (int(page)-1)*300 + 1
				users = json.loads(model.getLastUser(city,cursor))
		else:
			page = 1
			users = json.loads(model.getUser(city))
		return render.user(users,city,last,page,chinesecity)
		

class Retrive:
	def GET(self):
		cursor = web.input().cursor
		req = web.input().city
		page= web.input().page
		cursor = (int(page)-1)*300 + int(cursor)
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
		#data = {'r':0,'user':user}
		return json.dumps(user)
	def POST(self):
		print web.input()
		id = web.input().id
		user = model.reduce_likes(id)
		#data = {'r':1,'user':user}
		return json.dumps(user)
if __name__ == "__main__":
	app.run()
