#!/usr/bin/env python
#coding=gbk
import pymongo
import json
from bson.json_util import dumps
from bson import ObjectId
import math
import random
con = pymongo.Connection('mongodb://zs:1621@momonvshen.com:27017',27017)
db = con.momo
user = db.user
list = []
import time
start = time.clock()
for user in db.user.find({"sex":"F"}):
	list.append(user['momoid'])
stop = time.clock()
print len(list)
print (stop - start)
start1 = time.clock()
for id in list:
	rad = random.random()
	db.user.update({"momoid":id},{"$set":{"random":rad}})
stop1 = time.clock()
print (stop1-start1)

