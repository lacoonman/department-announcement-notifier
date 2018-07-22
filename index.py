import json
import smtplib
from email.mime.text import MIMEText
import requests
from bs4 import BeautifulSoup
from crawling import getNoticePosts
from datetime import date, datetime
import pytz
import boto3
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError


# def get(event):
# 	user_id = event['queryStringParameters']['id']
# 	return {'body': {'id': user_id, 'name': 'test'}}


# def post(event):
# 	user_id = event['queryStringParameters']['id']
# 	body = event['body']
# 	header = event['headers']
# 	return {'body': {'id': user_id, 'header': header, 'body': body}}


# route_map = {
# 	'/test': {
# 		'GET': get,
# 		'POST': post
# 	}
# }


# def router(event):
# 	controller = route_map[event['path']][event['httpMethod']]

# 	if not controller:
# 		return {'body': {'Error': 'Invalid Path'}}

# 	return controller(event)


# def handler(event, context):
# 	#return {'event' : str(event), 'context' : str(context)}
# 	#return {'body': json.dumps(event)}
# 	result = router(event)
# 	return {'body': json.dumps(result)}

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def handler(event, context):
	# 공지사항 게시판을 크롤링
	posts = getNoticePosts()
	# dynamo DB
	dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
	NoticeBoard = dynamodb.Table('NoticeBoard')
	# 크롤링된 게시글을 문자열로 변환해 메일로 전송
	log = ''
	body = ''
	for one_post in posts:
		if one_post.number != '공지':
			# 데이터베이스에 Item이 있는지 확인
			response = NoticeBoard.get_item(
				Key={
					'number': int(one_post.number)
				}
			)
			try:
				response['Item']
			# 데이터베이스에 Item이 없으면 Item을 추가하고 메일로 전송
			except Exception as e:
				NoticeBoard.put_item(
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
		send_mail(body)
	return log

if __name__ == '__main__':
	event = ''
	context = ''
	handler(event, context)