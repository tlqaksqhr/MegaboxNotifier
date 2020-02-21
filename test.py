# -*- coding: utf-8 -*-

import megabox

data = megabox.getBookingMovieListIDByDate("20200219")

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

print(megabox.addMovieDate(data, users_tag))
print(megabox.getCinemas("20200223","20004000"))

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