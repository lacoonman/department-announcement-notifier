from crawling import getPosts
from notice import send_mail
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


def newPostsToString(posts, table, title):
	# 크롤링된 게시글을 문자열로 변환
	body = ''
	for one_post in posts:
		if one_post.number != '공지':
			# 데이터베이스에 Item이 있는지 확인
			response = table.get_item(
				Key={
					'number': int(one_post.number)
				}
			)
			try:
				response['Item']
			# 데이터베이스에 Item이 없으면 Item을 추가하고 메일 본문에 추가
			except Exception as e:
				table.put_item(
					Item={
						'number': int(one_post.number),
						'title': str(one_post.title),
						'link': str(one_post.link),
						'writer': str(one_post.writer),
						'date': str(one_post.date),
						'views': str(one_post.views)
					}
				)
				body += str(one_post)
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
	NoticeTitle = '=' * 20 + ' 공지사항 ' + '=' * 20 + '\n' * 2
	NoticeBoard = dynamodb.Table('NoticeBoard')
	NoticePosts = getPosts(NOTICE)
	NoticeBody = newPostsToString(NoticePosts, NoticeBoard, NoticeTitle)
	if NoticeBody != '':
		body += '\n\n'
		body += NoticeBody
	# 학사 게시판
	CourseTitle = '=' * 20 + ' 학사 ' + '=' * 20 + '\n' * 2
	CourseBoard = dynamodb.Table('CourseBoard')
	CoursePosts = getPosts(COURSE)
	CourseBody = newPostsToString(CoursePosts, CourseBoard, CourseTitle)
	if CourseBody != '':
		body += '\n\n'
		body += CourseBody
	# ABEEK 게시판
	AbeekTitle = '=' * 20 + ' ABEEK ' + '=' * 20 + '\n' * 2
	AbeekBoard = dynamodb.Table('AbeekBoard')
	Abeekposts = getPosts(ABEEK)
	AbeekBody = newPostsToString(Abeekposts, AbeekBoard, AbeekTitle)
	if AbeekBody != '':
		body += '\n\n'
		body += AbeekBody

	# 채용정보 게시판
	#CareerTitle = '=' * 20 + ' 채용정보 ' + '=' * 20 + '\n' * 2
	#CareerBoard = dynamodb.Table('CareerBoard')
	#CareerPosts = getPosts(CAREER)

	# 새 게시글이 있으면 메일로 전송
	if body != '':
		send_mail(body)

	return log

if __name__ == '__main__':
	event = ''
	context = ''
	handler(event, context)