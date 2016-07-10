import json
from indeed import IndeedClient

client = IndeedClient('9093816856988990')

params = {
    'q' : "part time",
    'l' : "san jose",
    'userip' : "173.224.162.79",
    'useragent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2)"
}

search_response = client.search(**params)
print json.dumps(search_response,indent=4)
