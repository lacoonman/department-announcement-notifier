import json
import requests
from bs4 import BeautifulSoup

# URL 목록
NOTICE = 'http://computer.knu.ac.kr/07_sub/01_sub.html'
COURSE = 'http://computer.knu.ac.kr/07_sub/01_sub_2.html'
ABEEK = 'http://computer.knu.ac.kr/07_sub/01_sub_3.html'
CAREER = 'http://computer.knu.ac.kr/07_sub/01_sub_4.html'

# 크롤링 URL
URL = CAREER

response = requests.get(CAREER)
html_doc = response.text
soup = BeautifulSoup(html_doc, 'html.parser')

# html 문서에서 table 탐색
tables = soup.findAll('table')
f1 = open('f1.txt', 'w+', encoding='utf-8')
count = 0
for table in tables:
	f1.write('== {0} == \n'.format(count))
	f1.write('{0}\n\n'.format(table.prettify()))
	count += 1
f1.close()
## 결과 ##
# 24 ==> 공지 게시글 + 비공지 게시글
# 25~34 ==> 비공지 게시글



# tables[24]에서 tr 탐색
trs = tables[24].findAll('tr')
f2 = open('f2.txt', 'w+', encoding='utf-8')
count = 0
for tr in trs:
	f2.write('== {0} == \n'.format(count))
	f2.write('{0}\n\n'.format(tr.prettify()))
	count += 1
f2.close()
## 결과 ##
# 1, 3, 5, ... 에 유의미한 게시글 정보 존재
# 1번은 목차


# 각각의 홀수번째에 tr의 td에서 정보를 추출
f3 = open('f3.txt', 'w+', encoding='utf-8')
count = 0
for tr in trs:
	if count % 2 == 1:
		f3.write('========== {0} ========== \n'.format(count))
		tds = tr.findAll('td')
		incount = 0
		for td in tds:
			f3.write('= {0} = \n'.format(incount))
			f3.write('{0}\n'.format(td.prettify()))
			incount += 1
	count += 1
f3.close()
## 결과 ##
# 0번 td -> 번호(공지 = 공지)
# 1번 td -> 제목
# 2번 td -> 작성자
# 3번 td -> 작성일
# 4번 td -> 조회수
# 다만 홀수 게시글이 항상 유의미하지 않음 -> td의 개수를 세어 유의미한 게시글인지 판단(5개)


# td의 개수를 통해서 유의미한 게시글인지 판단
f4 = open('f4.txt', 'w+', encoding='utf-8')
count = 0
for tr in trs:
	tds = tr.findAll('td')
	if len(tds) > 4:
		f4.write('========== {0} ========== \n'.format(count))
		incount = 0
		for td in tds:
			f4.write('= {0} = \n'.format(incount))
			f4.write('{0}\n'.format(td.prettify()))
			incount += 1
	count += 1
f4.close()
## 결과 ##
# 공지 게시글은 td가 5개(0~4)
# 비공지 게시글은 TD가 6개(0~5)
# 제목이 2(1~2)번 나옴 -> 그 중 기존(공지)와 유사한 형식을 가진 것은 2번 td


##### 정보 종합 #####
## 번호 ##
# 공지는 td
# 비공지는 td

## 제목 ##
# 공지는  td->a->b
# 비공지는 td->a

## 작성자 ##
# 공지는 td
# 비공지는 td

## 작성일 ##
# 공지는 td
# 비공지는 td

## 조회수 ##
# 공지는 td
# 비공지는 td


# 지금까지 얻은 정보를 종합해서 태그가 아닌 파싱된 정보로 출력
# td의 개수를 통해서 유의미한 게시글인지 판단
f5 = open('f5.txt', 'w+', encoding='utf-8')
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
		f5.write('========== {0} ========== \n'.format(count))
		# 번호 출력
		f5.write('번호 : {0} \n'.format(tds[incount].get_text()))
		incount += 1
		# 공지가 아니면 인덱스를 +1 해줌
		if not isNotice:
			incount += 1
		# 제목 출력
		if isNotice:
			f5.write('제목 : {0} \n'.format(tds[incount].find('b').string))
		else :
			f5.write('제목 : {0} \n'.format(tds[incount].find('a').string))
		f5.write('링크 : {0} \n'.format(URL + tds[incount].find('a')['href']))
		incount += 1
		# 작성자 출력
		f5.write('작성자 : {0} \n'.format(tds[incount].string))
		incount += 1
		# 작성일 출력
		f5.write('작성일 : {0} \n'.format(tds[incount].string))
		incount += 1
		# 조회수 출력
		f5.write('조회수 : {0} \n'.format(tds[incount].string))
		incount += 1
		# 개수 + 1
		count += 1
f5.close()