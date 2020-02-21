import requests

url = "https://megabox.co.kr/on/oh/ohb/SimpleBooking/selectBokdList.do"
url_min_date = "https://megabox.co.kr/on/oh/ohb/SimpleBooking/selectMinBokdAbleDe.do"


# TODO : paramater 넣는 부분 builder pattern 써서 만들기..


# date : "20200219"
def getBookingMovieListIDByDate(date):
	param_data = {
		"playDe": date,
		"onLoad":"Y"
	}
	
	req = requests.post(url,json = param_data)
	return req.json()['movieList']


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

def getMovieDate(date, movie_code):
	param_data = {
		"arrMovieNo":movie_code,
		"playDe":date,
		"brchNoListCnt":0,
		"movieNo1":movie_code
	}
	req = requests.post(url_min_date,json = param_data)
	dates = req.json()['minBokdAbleDeList']

	filter_func = lambda items: {
		item : items[item] for item in items 
		if item == 'playDe'
	}

	return [filter_func(date_item) for date_item in dates]


def addMovieDate(data, users_tag):
    matched_list = getMatchedMovieByAllUser(users_tag, data)

    merge_func = lambda item : {**item, **{'movie_dates' : getMovieDate('20200101',item['movieNo'])}}

    for matched_item in matched_list:
        matched_item['search_result'] = [merge_func(item) for item in matched_item['search_result']]
    
    return matched_list


def getCinemas(date, movie_code):
	param_data = {
		"arrMovieNo":movie_code,
		"playDe":date,
		"brchNoListCnt":0,
		"movieNo1":movie_code
	}
	req = requests.post(url,json = param_data)
	data = req.json()['areaBrchList']
	data = [item for item in data if item['brchFormAt'] == 'Y']

	return data


def getSeatCount(date, movie_code, cinema_code):
	param_data = {
		"arrMovieNo" : movie_code,
		"playDe" : date,
		"brchNoListCnt" : 1,
		"movieNo1": movie_code,
		"brchNo1": cinema_code,
		"spclbYn1" : "N"
	}
	req = requests.post(url,json = param_data)
	datas = req.json()['movieFormList']

	filter_func = lambda data: {
		item : data[item] for item in data 
		if item == 'playSchdlNo' or item == 'restSeatCnt'
	}

	hash_key = make_hashkey(cinema_code,movie_code)

	data = {hash_key : filter_func(data) for data in datas}

	return data

def make_hashkey(cinema_code, movie_code):
	return cinema_code + "_" +  movie_code