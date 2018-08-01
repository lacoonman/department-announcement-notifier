# Notice-College-Announcement
경북대학교 컴퓨터학부 공지사항 게시판을 크롤링하여 새 게시글 등록 시 등록된 메일 주소로 알림을 보내주는 프로그램입니다.

## 사용 라이브러리, 프레임워크, 플랫폼
- AWS Lambda  
- AWS dynamoDB  
- python boto3  
- python bs4  
- python requests  
- python pytz  

## 주의사항
AWS lambda에서 사용하기 위해서는 위의 파이썬 패키지들을 작업 디렉토리 안에 다운로드해야합니다.

## 동작 방식
1. Amazon Lamda의 CloudWatch Events Trigger를 사용하여 주기적으로 과 공지사항을 크롤링
2. 크롤링 결과 새 게시글이 추가되었으면 등록된 사용자에게 메일을 전송

## 모듈
### index.py
AWS Lambda에서 작동하는 handler를 가진 모듈
### crawling.py
학과 공지사항 게시판을 크롤링하는 기능을 가진 모듈
### notice.py
사용자에게 알림(메일)을 보내는 기능을 가진 모듈
### database.py
AWS dynamoDB에 접근하는 기능을 가진 모듈

## 개발 기록
1. 학과 공지사항 게시판에 새 게시글이 추가되면 텍스트로 젼환하여 정해진 메일로 일괄 전송
2. 학사, ABEEK 게시판 추가
3. 채용정보 게시판 추가, 공지 게시글은 해석에서 제거
4. 게시글 번호에 추가적으로 제목도 확인하여 게시글 수정, 삭제 여부 확인
5. (dynamoDB에 등록된)다수의 사용자에게 메일 전송 기능 추가