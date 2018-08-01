from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import requests
import boto3
import decimal
import json

def scanDB(table):
	response = table.scan(
		ProjectionExpression="email"
	)

	items = []

	# 항목의 첫 페이지 스캔
	for item in response['Items']:
		items.append(item)
		print(item)

	# 데이터가 많아서 한 페이지를 넘을 경우
	while 'LastEvaluateKey' in response:
		response = table.scan(
			ExclusiveStartKey=response['LastEvaluteKey']
		)

		for item in response['Items']:
			items.append(item)
			print(item)

	return items

	# fe = Key('year').between(1950, 1959)
	# pe = "#yr, title, info.rating"
	# # Expression Attribute Names for Projection Expression only.
	# ean = { "#yr": "year", }
	# esk = None

	# response = table.scan(
	#     FilterExpression=fe,
	#     ProjectionExpression=pe,
	#     ExpressionAttributeNames=ean
	# )

def readDB(table, post):
	response = table.get_item(
		Key={
			'number': int(post.number)
		}
	)

def writeDB(table, post):
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

def updateDB(table, post):
	table.update_item(
		Key={
			'number': int(post.number)
		},
		UpdateExpression="set title=:t, link=:l, writer=:w, #dt=:d, #vw=:v",
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
	body += str(post)
	body += '\n'