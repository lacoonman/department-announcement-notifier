from crawling import getPosts
from notice import send_mail
from database import scanDB, readDB, writeDB, updateDB
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from bs4 import BeautifulSoup
import requests
import boto3
import decimal
import json


class DecimalEncoder(json.JSONEncoder):
	def default(self, o):
		if isinstance(o, decimal.Decimal):
			if abs(o) % 1 > 0:
				return float(o)
			else:
				return int(o)
		return super(DecimalEncoder, self).default(o)


def getTitleString(boardname):
	return '<' + boardname + '>' + '\n' * 2


def newPostsToString(posts, table, title):
	print(title)
	# 크롤링된 게시글을 문자열로 변환
	body = ''
	for post in posts:
		if post.number != '공지':
			# 데이터베이스에서 데이터를 읽음
			response = table.get_item(
				Key={
					'number': int(post.number)
				}
			)
			# 데이터베이스에서 항목이 있는 경우
			if 'Item' in response:
				item = response['Item']
				# 항목이 있으면서 제목이 같을 경우
				if item['title'] == str(post.title):
					#print(json.dumps(item, indent=4, cls=DecimalEncoder))
					print("Read Item")
					print('number : {0}\ntitle :{1}\n'.format(item['number'], item['title']))
				# 항목은 있지만 제목이 다를 경우(기존의 게시글이 삭제되고 새 게시글이 올라왔을 경우, 수정되었을 경우)
				else:
					# 항목을 업데이트, 메일에 추가
					table.update_item(
						Key={
							'number': int(post.number)
						},
						UpdateExpression="set title=:t, link=:l, writer=:w, #dt=:d, #vw=:v",
						# UpdateExpression에서 예약어가 있기 때문에 문자열을 대체
						ExpressionAttributeNames={
							'#dt':'date',
							'#vw':'views'
						},
						ExpressionAttributeValues={
							':t': str(post.title),
							':l': str(post.link),
							':w': str(post.writer),
							':d': str(post.date),
							':v': str(post.views)
						},
						ReturnValues="UPDATED_NEW"
					)
					print("Update Item")
					print('number : {0}\ntitle :{1}\n'.format(item['number'], item['title']))
					body += str(post)
					body += '\n'
			# 데이터베이스에 항목이 없는 경우
			else:
				# 항목을 삽입, 메일에 추가
				print("Insert Item")
				table.put_item(
					Item={
							'number': int(post.number),
							'title': str(post.title),
							'link': str(post.link),
							'writer': str(post.writer),
							'date': str(post.date),
							'views': str(post.views)
						}
				)
				body += str(post)
				body += '\n'

	if body != '':
		body = title + body

	return body


def handler(event, context):
	# 크롤링 할 URL
	NOTICE = 'http://computer.knu.ac.kr/07_sub/01_sub.html'
	COURSE = 'http://computer.knu.ac.kr/07_sub/01_sub_2.html'
	ABEEK = 'http://computer.knu.ac.kr/07_sub/01_sub_3.html'
	CAREER = 'http://computer.knu.ac.kr/07_sub/01_sub_4.html'

	# 로그 string
	log = ''

	# 메일 body
	body = ''

	# dynamo DB
	dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
	# 공지사항 게시판
	NoticeTitle = getTitleString('공지사항')
	NoticeBoard = dynamodb.Table('NoticeBoard')
	NoticePosts = getPosts(NOTICE)
	NoticeBody = newPostsToString(NoticePosts, NoticeBoard, NoticeTitle)
	if NoticeBody != '':
		body += '\n\n'
		body += NoticeBody
	# 학사 게시판
	CourseTitle = getTitleString('학사')
	CourseBoard = dynamodb.Table('CourseBoard')
	CoursePosts = getPosts(COURSE)
	CourseBody = newPostsToString(CoursePosts, CourseBoard, CourseTitle)
	if CourseBody != '':
		body += '\n\n'
		body += CourseBody
	# ABEEK 게시판
	AbeekTitle = getTitleString('ABEEK')
	AbeekBoard = dynamodb.Table('AbeekBoard')
	AbeekPosts = getPosts(ABEEK)
	AbeekBody = newPostsToString(AbeekPosts, AbeekBoard, AbeekTitle)
	if AbeekBody != '':
		body += '\n\n'
		body += AbeekBody

	# 채용정보 게시판
	CareerTitle = getTitleString('채용정보')
	CareerBoard = dynamodb.Table('CareerBoard')
	CareerPosts = getPosts(CAREER)
	CareerBody = newPostsToString(CareerPosts, CareerBoard, CareerTitle)
	if CareerBody != '':
		body += '\n\n'
		body += CareerBody

	# 새 게시글이 있으면 메일로 전송
	if body != '':
		send_mail(body)

	return log

if __name__ == '__main__':
	event = ''
	context = ''
	handler(event, context)