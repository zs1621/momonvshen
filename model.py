#!/usr/bin/env python
#coding=utf-8
import pymongo
from bson.json_util import dumps
from bson import ObjectId
con = pymongo.Connection('mongodb://****:****@****:****',*****)

db = con.momo

user = db.user

def getPhotos(req):
	return dumps(db.user.find_one({"momoid":req},{'photos'}))
def getTop(req):
	return dumps(db.user.find({"sex":"F","scity":req},{'name','photos','scity','_id','likes'}).limit(40).sort("likes",pymongo.DESCENDING))
def getTopPubu(req,cursor):
	return dumps(db.user.find({"sex":"F","scity":req},{'name','photos','scity','_id','likes'}).limit(30).skip(cursor).sort("likes",pymongo.DESCENDING))
def getCount(req):
	return db.user.find({"sex":"F","scity":req}).count()
def getUser(req):
	return dumps(db.user.find({"sex":"F","scity":req},{'name','photos','scity',"_id","likes"}).limit(30).sort("random",pymongo.DESCENDING))
def getRandomUser(req,random):
	return dumps(db.user.find({"sex":"F","scity":req,"random":{"$gt":random}}).limit(30))
def getLastUser(req,cursor):
	return dumps(db.suer.find({"sex":"F","scity":req},{'name','photos','scity',"_id","likes"}).skip(cursor).sort("random",pymongo.DESCENDING))
def getLimitUser(req,cursor):
	return dumps(db.user.find({"sex":"F","scity":req},{'name','photos','scity',"_id","likes"}).limit(30).skip(cursor).sort("random",pymongo.DESCENDING))
def getUserProfile(req):
	return dumps(db.user.find({"_id":ObjectId(req)},{'name','photos','scity','momoid',"hometown","hangout","aboutme","school","constellation","job","photos","sign","website","age","company","likes"}))
def add_likes(req):
	db.user.update({"_id":ObjectId(req)},{"$inc":{"likes":1}})
	return dumps(db.user.find({"_id":ObjectId(req)},{"likes"}))
		
def reduce_likes(req):
	db.user.update({"_id":ObjectId(req)},{"$inc":{"likes":-1}})
	return dumps(db.user.find({"_id":ObjectId(req)},{"likes"}))

