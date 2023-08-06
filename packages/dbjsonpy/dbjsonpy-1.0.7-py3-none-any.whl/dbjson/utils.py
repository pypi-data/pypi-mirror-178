import json

def union(json1, json2):
	dict1 = json.loads(json1)
	dict2 = json.loads(json2)
	list1 = dict1["data"]
	list2 = dict2["data"]
	# data = list1.union(list2).all()
	# data = list(set(list1) | set(list2))
	
	return data
