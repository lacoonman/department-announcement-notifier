from email.mime.text import MIMEText
from IDPW import ID, PW
from datetime import date, datetime
from email.mime.text import MIMEText
import pytz
import smtplib


def send_mail(body=''):
	# SMTP를 활용한 메일 전송
	smtp = smtplib.SMTP('smtp.gmail.com', 587)
	smtp.ehlo()      # say Hello
	smtp.starttls()  # TLS 사용시 필요
	smtp.ehlo()
	smtp.login(ID, PW)
	
	# 본문 
	#msg = MIMEText('본문')
	msg = MIMEText(body)
	# 제목
	#msg['Subject'] = '제목'
	fmt = '%Y-%m-%d %H:%M:%S'
	utc = pytz.timezone('UTC')
	seoul = pytz.timezone('Asia/Seoul')
	utc_dt = utc.localize(datetime.now())
	seoul_dt = utc_dt.astimezone(seoul)
	msg['Subject'] = '{0} 학과 공지사항입니다.'.format(seoul_dt.strftime(fmt))
	msg['To'] = 'teakan7179@gmail.com'
	smtp.sendmail('knucse.mailsender@gmail.com', 'teakan7179@gmail.com', msg.as_string())
	
	smtp.quit()