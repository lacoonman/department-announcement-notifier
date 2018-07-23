import json
import requests
from bs4 import BeautifulSoup

class Post(object):
	def __init__(self, number='', title='', link='', writer='', date='', views=''):
		self.number = number
		self.title = title
		self.link = link
		self.writer = writer
		self.date = date
		self.views = views
	
	def __str__(self):
		pretty = '번호 : {0}\n제목 : {1}\n링크 : {2}\n작성자 : {3}\n작성일 : {4}\n조회수 : {5}\n'.format(self.number, self.title, self.link, self.writer, self.date, self.views)
		return pretty
	
	def getDic(self):
		Item = {
			'number': int(self.number),
			'title': str(self.title),
			'link': str(self.link),
			'writer': str(self.writer),
			'date': str(self.date),
			'views': str(self.views)
		}
		return Item


def getPosts(URL):
	response = requests.get(URL)
	html_doc = response.text
	soup = BeautifulSoup(html_doc, 'html.parser')

	# html 문서에서 table 탐색
	tables = soup.findAll('table')

	# tables[24]에서 tr 탐색
	trs = tables[24].findAll('tr')

	# 게시글 배열
	posts = []
	# tr의 집합에서 정보 추출
	count = 0
	existIndex = True
	for tr in trs:
		# 이번 tr에 있는 td를 전부 수집
		tds = tr.findAll('td')
		# 유의미한 정보가 있는 tr인지 판단(td가 5개 이상일 경우)
		if len(tds) > 4:
			# 첫 번째는 목차이므로 패스
			if existIndex:
				existIndex = False
				continue
			# 공지 여부 정보를 저장
			isNotice = True if tds[0].string == '공지' else False
			incount = 0
			# 번호
			number = tds[incount].get_text()
			incount += 1
			# 공지이면 정보를 읽지 않음
			if isNotice:
				continue
			# 공지가 아니면 인덱스를 +1 해줌
			else:
				incount += 1
			# 제목
			title = ''
			if isNotice:
				title = tds[incount].find('b').string
			else:
				title = tds[incount].find('a').string
			link = URL + tds[incount].find('a')['href']
			incount += 1
			# 작성자 출력
			writer = tds[incount].string
			incount += 1
			# 작성일 출력
			date = tds[incount].string
			incount += 1
			# 조회수 출력
			views = tds[incount].string
			incount += 1
			# 개수 + 1
			count += 1
			# posts 배열에 게시글 추가
			posts.append(Post(number, title, link, writer, date, views))
	return posts


if __name__ == '__main__':
	# 크롤링 할 URL
	NOTICE = 'http://computer.knu.ac.kr/07_sub/01_sub.html'
	COURSE = 'http://computer.knu.ac.kr/07_sub/01_sub_2.html'
	ABEEK = 'http://computer.knu.ac.kr/07_sub/01_sub_3.html'
	CAREER = 'http://computer.knu.ac.kr/07_sub/01_sub_4.html'

	# 함수 실행
	posts = getPosts(CAREER)
	# 표준출력
	for post in posts:
		print(post)