from yelpauthdata import Yelp


class Cheating(object):
	def __init__(self, target):
		self.target=target

	def targets(self):
		yelp=Yelp()
		client=yelp.clientAuth()
		params = {'term': self.target, 'lang': 'en','deals_filter':'true'}
		response=client.search('San Jose', **params)
		print(response.businesses)
		ret=[]
		# for i in range(min(3,len(response.businesses))):
		# 	print(response.businesses[i].name)
		return response.businesses[:min(3,len(response.businesses))]



if '__name__'=='main':
	obj = cheating("doorknob")
	client=obj.targets()
