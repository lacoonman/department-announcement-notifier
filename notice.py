from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from database import scanDB
from email.mime.text import MIMEText
from IDPW import ID, PW
from datetime import date, datetime
from email.mime.text import MIMEText
import boto3
import pytz
import smtplib


def send_mail(body=''):
	# dynamo DB
	dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
	# 이메일 주소 데이터베이스 접근
	emailTable = dynamodb.Table('NCA-Email')
	# 모든 이메일 주소를 스캔
	items = scanDB(emailTable)
	# 데이터베이스 항목에서 이메일 주소 리스트를 생성
	emails = []
	for item in items:
		emails.append(str(item['email']))

	# SMTP를 활용한 메일 전송
	smtp = smtplib.SMTP('smtp.gmail.com', 587)
	smtp.ehlo()      # say Hello
	smtp.starttls()  # TLS 사용시 필요
	smtp.ehlo()
	smtp.login(ID, PW)
	
	# 본문 
	#msg = MIMEText('본문')
	msg = MIMEText(body)
	fmt = '%Y-%m-%d %H:%M:%S'
	utc = pytz.timezone('UTC')
	seoul = pytz.timezone('Asia/Seoul')
	utc_dt = utc.localize(datetime.now())
	seoul_dt = utc_dt.astimezone(seoul)
	# 제목
	msg['Subject'] = '{0} 학과 공지사항입니다.'.format(seoul_dt.strftime(fmt))
	# 수신자
	msg['To'] = 'teakan7179@gmail.com'
	# 메일 전송
	print(emails)
	smtp.sendmail('knucse.mailsender@gmail.com', emails, msg.as_string())
	
	smtp.quit()