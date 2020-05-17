# Introduction
회원정보와 주문정보를 활용하여 DB modeling, API 구현, Unit test 코드 작성

<br>

# Technologies
* Python 3.8
* Django
* MySQL
* CORS headers
* bcrypt
* jwt
* Docker

<br>

# DB Modeling

![DB Modeling](https://user-images.githubusercontent.com/53142539/82083118-22ff6080-9724-11ea-9621-9967df6af4d0.png)

<br>

# Features
## _User_
### Sign-up (POST)
* IntegrityError를 사용하여 이메일 중복 체크
* Gender table에 존재하지 않는 성별이 입력되면 error를 return
* validate_email, validate_integer를 사용하여 이메일과 전화번호 형식 체크
* 이름, 닉네임, 비밀번호의 형식을 체크하는 validator 작성
* bcrypt로 비밀번호 암호화하여 저장

### Sign-in (POST)
* 이메일 필드를 unique 하게 하여 중복값이 없도록 설정 및 로그인 아이디로 사용
* jwt를 사용하여 로그인 성공 시 access token 발행

### Log-out (GET)
* 로그인 된 user인지 먼저 체크하는 decorator 작성
* request.session.flush()로 해당 request의 session을 reset

### User info (GET)
* 로그인 된 user의 계정 정보 return

<br>

## _Order_
### Order (POST)
* 로그인 한 회원의 주문하기 기능
* 제품명에 emoji가 들어갈 수 있도록 db 설정

### Order Detail (GET)
* url 뒤에 query parameter로 user id를 받아, 해당 회원의 주문 목록 조회
* 가장 최근에 결제한 순서대로 결과값 return

### Order List (GET)
* 회원들의 마지막 주문 정보 list 조회
* limit, page 값을 query parameter로 받아 pagination 구현
* name, email 값을 query parameter로 받아 검색 기능 구현

<br>

# API Documentation
## [API Documentation using Postman](https://documenter.getpostman.com/view/10633619/SzmmTuNL?version=latest)

<br>

# Settings

### my_settings.py 수정
* DATABASES의 아래 2가지 속성 수정
```
'USER'    : 'root',
'PASSWORD': 'password',
```

### MySQL 테이블 생성

```
CREATE DATABASE project DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
use project;

INSERT INTO genders VALUES (1, 'Woman');
INSERT INTO genders VALUES (2, 'Man');
```

### Docker 사용
```
sudo docker pull hongdev22/project:0.1

sudo docker run --name project -d -p 8000:8000 hongdev22/project:0.1
```
