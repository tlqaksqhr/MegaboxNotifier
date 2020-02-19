import requests

url = "https://megabox.co.kr/on/oh/ohb/SimpleBooking/selectBokdList.do"
url_min_date = "https://megabox.co.kr/on/oh/ohb/SimpleBooking/selectMinBokdAbleDe.do"

def getBookingMovieListIDByDate(date):
	param_data = {
		"playDe": date,# "20200219",
		"incomeMovieNo":"",
		"onLoad":"Y",
		"sellChnlCd":"",
		"incomeTheabKindCd":"",
		"incomeBrchNo1":"",
		"incomePlayDe":""
	}
	req = requests.post(url,json = param_data)
	return req.json()['movieList']


def getMovieDate(date, movie_code):
	param_data = {
		"arrMovieNo":movie_code,
		"playDe":date,
		"brchNoListCnt":0,
		"brchNo1":"",
		"brchNo2":"",
		"brchNo3":"",
		"areaCd1":"",
		"areaCd2":"",
		"areaCd3":"",
		"spclbYn1":"",
		"spclbYn2":"",
		"spclbYn3":"",
		"theabKindCd1":"",
		"theabKindCd2":"",
		"theabKindCd3":"",
		"brchAll":"",
		"brchSpcl":"",
		"movieNo1":movie_code,
		"movieNo2":"",
		"movieNo3":"",
		"sellChnlCd":""
	}
	req = requests.post(url_min_date,json = param_data)
	return req.json()

def getBookingMovieListByDate():
	pass




'''

param

user_tag = {
	'user' : 'xxxx',
	'tags' : [
		'yyyyx',
		'yyyyy',
		...
	]
}

return_value

user_value = [
	{
		'user' : 'xxxxxx',
		'search_result' : [
			{'movieNo': '20004000', 'movieNm': 'yyyyy'}
		]
	},
	{
		'user' : 'xxxxxy',
		'search_result' : [
			{'movieNo': '20004000', 'movieNm': 'yyyyy'}
		]
	},
	...
]

'''

def getMatchedMovieByAllUser(users_tag, data):
	search_result_list = []

	filter_func = lambda items: {
		item : items[item] for item in items 
		if item == 'movieNo' or item == 'movieNm'
	}

	mapping_item = lambda tag: [
		filter_func(item) for item in data 
		if tag in item['movieNm']
	][0]

	for user_tag in users_tag:
		filtered_data = [mapping_item(tag) for tag in user_tag['tags']]
		# remove duplicate search result
		filtered_data = list({item['movieNo'] : item for item in filtered_data}.values())
		search_result_list.append({'user' : user_tag['user'], 'search_result' : filtered_data})

	

	return search_result_list

data = getBookingMovieListIDByDate("20200219")

users_tag = [
	{
	'user' : 'Alex',
	'tags' : [
		'러브라이브 선샤인',
		'First LOVELIVE',
	]},
	{
	'user' : 'Kim',
	'tags' : [
		'First LOVELIVE',
		'러브라이브 선샤인',
	]},
]

matched_list = getMatchedMovieByAllUser(users_tag, data)
print(matched_list)