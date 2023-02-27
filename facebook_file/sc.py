# import json
# import facebook
# def main():
# 	token = "EAAG5oU7ZATZAUBAO1hZCtbhegzFTTeczZCL8LVDyouf4809cXV5GVFuxkZAGRdgO0A06rvC55aMlZBSuBizzuFyQtm89ZCn9PMX0DAqrKrJcdZAVjLqrlzNHFX7xW3G9yQlo0lPxBZCqhN7wbnvneoYLhjFjdsXtbe8Tg15XXOumPAX65q8b343rbzREdmnVnnGCZA5piMw5im5YQEYdPlaoZCT"
# 	graph = facebook.GraphAPI(token)
# 	page_name = "نادي الفنون الجميلة : دار الشباب بالعالية"
	
# 	# list of required fields
# 	fields = ['id','name','about','likes','link','band_members']
	
# 	fields = ','.join(fields)
	
# 	page = graph.get_object(page_name, fields=fields)
		
# 	print(json.dumps(page,indent=4))
# if __name__ == '__main__':
# 	main()
