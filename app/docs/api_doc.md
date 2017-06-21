## 사용 기술
- python 2.7
- python flask 및 관련 라이브러리
- python sqlalchemy(ORM)

<br>

## 서버 주소
### `http://calendar.jungi.me`


<br><br>

# calendar API Reference

</br></br></br>
## ** API/WEB base URL **
- 현재 api version : v1
- API URL : `http://calendar.jungi.me/api/{api_version}`

    
<br/>


## ** Request/Response Format**

## **HTTP Method**
- API : `GET, POST, PUT, DELETE`


## **Request/Response Format**

### Request
Method POST, PUT, DELETE
- API : JSON - `Content-type: application/json`

Method GET
- API : URL Query String  


### Response
- JSON

<br/><br/>

## **Authorization**

### **권한 부여 방식**
- 로그인 API를 통해 사용자 인증 성공시, 서버에서는 사용자별 고유키값, Token 발급일시, 만료일시 등의 정보를 Encode하여 JSON Web Token 형식으로 Access Token을 발급한다.
- 이후 App에서는 접근 권한(로그인)이 필요한 API 호출시 HTTP Header에 `X-calendar-access-token` 라는 Key에 해당 Token값을 설정하여 호출한다.
- 서버에서는 API 호출시 Header로 넘어온 Token값을 Decode하여 유효성 여부를 검증하여, API에 대한 접근을 허용 혹은 차단한다.

### **Token Format**
- JSON Web Token (https://en.wikipedia.org/wiki/JSON_Web_Token)


<br/><br/>


## ** API 리스트 **

| No | Resource Name | URI | token 필요 여부 | HTTP Method |
| --- | --- | --- | --- | --- |
| 1 | 유저생성 및 토큰 발급 | /api/v1/user/ |  | POST |
| 2 | 자신의 캘린더에 표시할 캘린더 그룹 등록 및 수정| /api/v1/user/calendar/group | O | POST |
| 3 | (자신의 캘린더)기본 월별 캘린더 - 이번달 일정 조회 | /api/v1/calendar/ | O | GET |
| 4 | (자신의 캘린더)다른 달로 이동 - 달 월별 일정 조회 | /api/v1/calendar/month | O | GET |
| 5 | (자신의 캘린더)일정 등록 | /api/v1/calendar/event | O | POST |
| 6 | (자신의 캘린더)일정 수정 | /api/v1/calendar/event | O | PUT |
| 7 | (자신의 캘린더)일정 삭제 | /api/v1/calendar/event | O | DELETE |
| 8 | (자신의 캘린더)오늘 일정 조회 | /api/v1/calendar/today | O | GET |
| 9 | (자신의 캘린더)특정 날짜 일정 조회 | /api/v1/calendar/date | O | GET |
| 10 | (자신의 캘린더)일정 검색 | /api/v1/calendar/search | O | GET |
| 11 | (자신의 캘린더)생일 등록 | /api/v1/calendar/birthday | O | PUT |
| 12 | 캘린더 그룹 추가 | /api/v1/group/ | O | POST |
| 13 | 캘린더 그룹 수정 | /api/v1/group/ | O | PUT |
| 14 | 캘린더 그룹 삭제(캘린더 그룹에 등록된 일정 전체 삭제) | /api/v1/group/ | O | DELETE |
| 15 | 캘린더 그룹 조회(내가 생성한 그룹) | /api/v1/group/ | O | GET |
| 16 | 캘린더 그룹 조회(모든 그룹 조회) | /api/v1/group/list | O | GET |
| 17 | 특정 그룹에 일정 등록 | /api/v1/group/event | O | POST |



<br/><br/>


## **공통 Response**
| Name	| Description |
| --- | --- |
| meta |  |
|   - code | 결과코드 |
|   - message | 결과메시지 |
| data | 결과값 집합 <br/> 반환할 결과값이 없거나 예외/에러 발생시 생략 |

Example :
```JSON
{
    "meta": {
        "code": 20000,
        "message": "SUCCESS"
    },
    "data": {
      ...
    }
}

```
<br/><br/>

 ## **기본 결과 코드**

| HTTP Status	| Code |	Message	| Description |
| --- | --- | --- | --- |
| 200 OK | 20000 | success |	성공 |
| 400  Bad Request	| 40000 |	invalid parameter	| 필수 파라미터 및 파라미터 형식 오류 | 
| 401  Unauthorized	| 40100	| invalid authorization	| 인증 오류
| 403  Forbidden	| 40300	| method not allowed	| 특정 HTTP Method가 허락되지 않은 경우 |
| 404  Not Found	 | 40400 | not found	 | 특정 리소스가 없는 경우|
| 500  Internal Server Error | 50000	 | internal server error	 | 서버 내부 에러 |


<br/><br/>

 ## **커스텀 결과 코드**

| HTTP Status	| Meta Code |	Message	| Description |
| --- | --- | --- | --- |
| 200 OK | 20010 | USER ID EXIST |	요청은 정상적이나, 이미 같은 email로 등록된 유저 있음 |
| 200 OK | 20010 | USER BIRTHDAY EXIST |	요청은 정상적이나, 이미 같은 email로 생일이 등록되어 있음 |
| 400  Bad Request	| 40001 |	INVALID PARAMETER	| 필수 파라미터 및 파라미터 형식 오류 | 
| 401  Unauthorized	| 40101	| MISSING HEADER	| 헤더에 access token 없음 |
| 401  Unauthorized	| 40102	| INVAILD TOKEN	| 올바른 access token이 아님 |
| 401  Unauthorized	| 40102	| UNAUTHORIZED REQUEST	| 권한이 없는 요청 |


<br><br>
## ** 아래의 response 값은 return data의 형식을 나타내는 것입니다. 결과 데이터의 값은 request의 파라미터들에 부합하지 않을수 있습니다. **

## 회원 API

### **회원 등록 API**

#### URI : /api/v1/`user/`

#### Header : 

#### Http Method : `POST`

#### **Parameters**


**Request**

| Name	| Description | Required | Type |
| --- | --- | --- | --- |
| useremail | 회원 email | O | string |
```json
{
 "usereamil" : "park@jungi.me"
}
```


**Response**

| Name	| Description | Required | Type |
| --- | --- | --- | --- |
| token | 발급된 access token | O | string |

```json
{
  "data": {
    "token" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJKVU5HSVBBUksiLCJ1c2VyZW1haWwiOiJwYXJrQGp1bmdpLm1lIiwiYXVkIjoiQ0FMRU5EQVJfQVBJIn0.8gpD2Wd-p26UuPVLHP9bLD9gbXo_nbP19rzO8N0N0zo"
  },
  "meta": {
    "code": 20000,
    "message": "SUCCESS"
  }
}
```
<br><br>



### **회원 캘린더 그룹 선택 API**

#### URI : /api/v1/`user/calendar/group`

#### Header : `token_required`

#### Http Method : `POST`

#### **Parameters**


**Request**

| Name	| Description | Required | Type |
| --- | --- | --- | --- |
| selected_group| 캘린더에 표시할 그룹 | O | string |
```json
{
 "selected_group" : "1,2,3" // 그룹 id를 구분해서 보냄, 표시할 그룹을 없애고자 할떄는 "0" 을 보냄
}
```

**Response**

| Name	| Description | Required | Type |
| --- | --- | --- | --- |


```json
// 성공시
{
  "meta": {
    "code": 20000,
    "message": "SUCCESS"
  }
}
```
<br><br>




## 캘린더 API

### **월별 캘린더 조회(이번달) API**

#### URI : /api/v1/`calendar/`

#### Header : `token_required`

#### Http Method : `GET`

#### **Parameters**


**Request**

| Name	| Description | Required | Type |
| --- | --- | --- | --- |


**Response**

| Name	| Description | Required | Type |
| --- | --- | --- | --- |
| event_list | 결과리스트 | O | JSONArray |
| - birthday | 생일여부(null 생일 아님, "1" 생일) | O | string or null |
| - created | 일정 등록 시간 | O | string |
| - updated | 일정 수정 시간 | O | string or null|
| - sdate | 일정 시작 시간 | O | string |
| - edate | 일정 종료 시간 | O | string |
| - useremail | 등록한 useremail | O | string |
| - subject | 일정 제목 | O | string |
| - id | 일정 event id| O | int |


```json
// 성공시
{
    [
        {
            "birthday": null,
            "created": "Mon, 19 Jun 2017 19:55:04 GMT",
            "edate": "Tue, 20 Jun 2017 12:00:00 GMT",
            "email": "park@jungi.me",
            "group": "2",
            "id": 25,
            "sdate": "Tue, 20 Jun 2017 09:00:00 GMT",
            "subject": "테스트 일정",
            "updated": null
        },
        {
            "birthday": null,
            "created": "Mon, 19 Jun 2017 20:13:47 GMT",
            "edate": "Tue, 20 Jun 2017 21:00:00 GMT",
            "email": "park@jungi.me",
            "group": null,
            "id": 26,
            "sdate": "Tue, 20 Jun 2017 20:00:00 GMT",
            "subject": "놀이동산",
            "updated": null
        }
    ],
    "meta": {
        "code": 20000,
        "message": "SUCCESS"
    }
}
```
<br><br>



### **월별 캘린더 조회(다른달로 이동) API**

#### URI : /api/v1/`calendar/month`

#### Header : `token_required`

#### Http Method : `GET`

#### **Parameters**


**Request**

| Name	| Description | Required | Type |
| --- | --- | --- | --- |
| year_month | 조회할 연도, 월 | O | query string | 
```
calendar.jungi.me/api/v1/calendar/month?year_month=2017-06
```

**Response**

| Name	| Description | Required | Type |
| --- | --- | --- | --- |
| event_list | 결과리스트 | O | JSONArray |
| - birthday | 생일여부(null 생일 아님, "1" 생일) | O | string or null |
| - created | 일정 등록 시간 | O | string |
| - updated | 일정 수정 시간 | O | string or null|
| - sdate | 일정 시작 시간 | O | string |
| - edate | 일정 종료 시간 | O | string |
| - useremail | 등록한 useremail | O | string |
| - subject | 일정 제목 | O | string |
| - id | 일정 event id| O | int |


```json
// 성공시
{
    [
        {
            "birthday": null,
            "created": "Mon, 19 Jun 2017 19:55:04 GMT",
            "edate": "Tue, 20 Jun 2017 12:00:00 GMT",
            "email": "park@jungi.me",
            "group": "2",
            "id": 25,
            "sdate": "Tue, 20 Jun 2017 09:00:00 GMT",
            "subject": "테스트 일정",
            "updated": null
        },
        {
            "birthday": null,
            "created": "Mon, 19 Jun 2017 20:13:47 GMT",
            "edate": "Tue, 20 Jun 2017 21:00:00 GMT",
            "email": "park@jungi.me",
            "group": null,
            "id": 26,
            "sdate": "Tue, 20 Jun 2017 20:00:00 GMT",
            "subject": "놀이동산",
            "updated": null
        }
    ],
    "meta": {
        "code": 20000,
        "message": "SUCCESS"
    }
}
```
<br><br>


### **특정 날짜 일정 조회 API**

#### URI : /api/v1/`calendar/date`

#### Header : `token_required`

#### Http Method : `GET`

#### **Parameters**


**Request**

| Name	| Description | Required | Type |
| --- | --- | --- | --- |
| date | 조회할 연도, 월, 일 | O | query string | 
```
calendar.jungi.me/api/v1/calendar/month?year_month=2017-06-20
```

**Response**

| Name	| Description | Required | Type |
| --- | --- | --- | --- |
| event_list | 결과리스트 | O | JSONArray |
| - birthday | 생일여부(null 생일 아님, "1" 생일) | O | string or null |
| - created | 일정 등록 시간 | O | string |
| - updated | 일정 수정 시간 | O | string or null|
| - sdate | 일정 시작 시간 | O | string |
| - edate | 일정 종료 시간 | O | string |
| - useremail | 등록한 useremail | O | string |
| - subject | 일정 제목 | O | string |
| - id | 일정 event id| O | int |


```json
// 성공시
{
    [
        {
            "birthday": null,
            "created": "Mon, 19 Jun 2017 19:55:04 GMT",
            "edate": "Tue, 20 Jun 2017 12:00:00 GMT",
            "email": "park@jungi.me",
            "group": "2",
            "id": 25,
            "sdate": "Tue, 20 Jun 2017 09:00:00 GMT",
            "subject": "테스트 일정",
            "updated": null
        },
        {
            "birthday": null,
            "created": "Mon, 19 Jun 2017 20:13:47 GMT",
            "edate": "Tue, 20 Jun 2017 21:00:00 GMT",
            "email": "park@jungi.me",
            "group": null,
            "id": 26,
            "sdate": "Tue, 20 Jun 2017 20:00:00 GMT",
            "subject": "놀이동산",
            "updated": null
        }
    ],
    "meta": {
        "code": 20000,
        "message": "SUCCESS"
    }
}
```
<br><br>


### **일정 등록 API**

#### URI : /api/v1/`calendar/event/`

#### Header : `token_required`

#### Http Method : `POST`

#### **Parameters**


**Request**

| Name	| Description | Required | Type |
| --- | --- | --- | --- |
| sdate| 일정 시작 일자 | O | "2017-06-19 20:00:00" 형식 / string |
| edate| 일정 종료 일자 | O | "2017-06-19 20:00:00" 형식 / string |
| subject | 일정 제목 | O | string |

```json
{
  "sdate" : "2017-06-19 20:00:00",
  "edate" : "2017-06-19 23:00:00",
  "subject" : "친구들과 약속"
}
```

**Response**

| Name	| Description | Required | Type |
| --- | --- | --- | --- |


```json
// 성공시
{
  "meta": {
    "code": 20000,
    "message": "SUCCESS"
  }
}
```
<br><br>


### **일정 수정 API**

#### URI : /api/v1/`calendar/event/`

#### Header : `token_required`

#### Http Method : `PUT`

#### **Parameters**


**Request**

| Name	| Description | Required | Type |
| --- | --- | --- | --- |
| sdate| 일정 시작 일자 | O | "2017-06-19 20:00:00" 형식 / string |
| edate| 일정 종료 일자 | O | "2017-06-19 20:00:00" 형식 / string |
| subject | 일정 제목 | O | string |
| event_id | 수정할 일정 id | O | int |

```json
{
  "sdate" : "2017-06-19 20:00:00",
  "edate" : "2017-06-19 23:00:00",
  "subject" : "친구들과 약속",
  "event_id" : 215
}
```

**Response**

| Name	| Description | Required | Type |
| --- | --- | --- | --- |


```json
// 성공시
{
  "meta": {
    "code": 20000,
    "message": "SUCCESS"
  }
}
```
<br><br>


### **일정 삭제 API**

#### URI : /api/v1/`calendar/event/`

#### Header : `token_required`

#### Http Method : `DELETE`

#### **Parameters**


**Request**

| Name	| Description | Required | Type |
| --- | --- | --- | --- |
| event_id | 삭제할 일정 id | O | int |

```json
{
  "event_id" : 215
}
```

**Response**

| Name	| Description | Required | Type |
| --- | --- | --- | --- |


```json
// 성공시
{
  "meta": {
    "code": 20000,
    "message": "SUCCESS"
  }
}
```
<br><br>

### **오늘 일정 조회 API**

#### URI : /api/v1/`calendar/today`

#### Header : `token_required`

#### Http Method : `GET`

#### **Parameters**


**Request**

| Name	| Description | Required | Type |
| --- | --- | --- | --- |



**Response**

| Name	| Description | Required | Type |
| --- | --- | --- | --- |
| event_list | 결과리스트 | O | JSONArray |
| - birthday | 생일여부(null 생일 아님, "1" 생일) | O | string or null |
| - created | 일정 등록 시간 | O | string |
| - updated | 일정 수정 시간 | O | string or null|
| - sdate | 일정 시작 시간 | O | string |
| - edate | 일정 종료 시간 | O | string |
| - useremail | 등록한 useremail | O | string |
| - subject | 일정 제목 | O | string |
| - id | 일정 event id| O | int |


```json
// 성공시
{
    [
      {
            "birthday": null,
            "created": "Mon, 19 Jun 2017 19:55:04 GMT",
            "edate": "Tue, 20 Jun 2017 12:00:00 GMT",
            "email": "park@jungi.me",
            "group": "2",
            "id": 25,
            "sdate": "Tue, 20 Jun 2017 09:00:00 GMT",
            "subject": "테스트 일정",
            "updated": null
        },
        {
            "birthday": null,
            "created": "Mon, 19 Jun 2017 19:55:04 GMT",
            "edate": "Tue, 20 Jun 2017 12:00:00 GMT",
            "email": "park@jungi.me",
            "group": "2",
            "id": 25,
            "sdate": "Tue, 20 Jun 2017 09:00:00 GMT",
            "subject": "테스트 일정",
            "updated": null
        }
    ],
    "meta": {
        "code": 20000,
        "message": "SUCCESS"
    }
}
```
<br><br>


### **특정 날짜 일정 API**

#### URI : /api/v1/`calendar/date`

#### Header : `token_required`

#### Http Method : `GET`

#### **Parameters**


**Request**

| Name	| Description | Required | Type |
| --- | --- | --- | --- |
| date | 조회할 연도, 월, 일 | O | query string | 
```
calendar.jungi.me/api/v1/calendar/month?date=2017-06-22
```

**Response**

| Name	| Description | Required | Type |
| --- | --- | --- | --- |
| event_list | 결과리스트 | O | JSONArray |
| - birthday | 생일여부(null 생일 아님, "1" 생일) | O | string or null |
| - created | 일정 등록 시간 | O | string |
| - updated | 일정 수정 시간 | O | string or null|
| - sdate | 일정 시작 시간 | O | string |
| - edate | 일정 종료 시간 | O | string |
| - useremail | 등록한 useremail | O | string |
| - subject | 일정 제목 | O | string |
| - id | 일정 event id| O | int |


```json
// 성공시
{
    [
        {
            "birthday": null,
            "created": "Mon, 19 Jun 2017 19:55:04 GMT",
            "edate": "Tue, 20 Jun 2017 12:00:00 GMT",
            "email": "park@jungi.me",
            "group": "2",
            "id": 25,
            "sdate": "Tue, 20 Jun 2017 09:00:00 GMT",
            "subject": "테스트 일정",
            "updated": null
        },
        {
            "birthday": null,
            "created": "Mon, 19 Jun 2017 20:13:47 GMT",
            "edate": "Tue, 20 Jun 2017 21:00:00 GMT",
            "email": "park@jungi.me",
            "group": null,
            "id": 26,
            "sdate": "Tue, 20 Jun 2017 20:00:00 GMT",
            "subject": "놀이동산",
            "updated": null
        }
    ],
    "meta": {
        "code": 20000,
        "message": "SUCCESS"
    }
}
```
<br><br>


### **일정 검색 API**

#### URI : /api/v1/`calendar/search`

#### Header : `token_required`

#### Http Method : `GET`

#### **Parameters**


**Request**

| Name	| Description | Required | Type |
| --- | --- | --- | --- |
| search_word | 조회할 연도, 월, 일 | O | query string | 
```
http://localhost:5000/api/v1/calendar/search?search_word=테스트
```

**Response**

| Name	| Description | Required | Type |
| --- | --- | --- | --- |
| event_list | 결과리스트 | O | JSONArray |
| - birthday | 생일여부(null 생일 아님, "1" 생일) | O | string or null |
| - created | 일정 등록 시간 | O | string |
| - updated | 일정 수정 시간 | O | string or null|
| - sdate | 일정 시작 시간 | O | string |
| - edate | 일정 종료 시간 | O | string |
| - useremail | 등록한 useremail | O | string |
| - subject | 일정 제목 | O | string |
| - id | 일정 event id| O | int |


```json
// 성공시
{
    [
        {
            "birthday": null,
            "created": "Mon, 19 Jun 2017 19:55:04 GMT",
            "edate": "Tue, 20 Jun 2017 12:00:00 GMT",
            "email": "park@jungi.me",
            "group": "2",
            "id": 25,
            "sdate": "Tue, 20 Jun 2017 09:00:00 GMT",
            "subject": "테스트 일정",
            "updated": null
        },
        {
            "birthday": null,
            "created": "Mon, 19 Jun 2017 20:13:47 GMT",
            "edate": "Tue, 20 Jun 2017 21:00:00 GMT",
            "email": "park@jungi.me",
            "group": null,
            "id": 26,
            "sdate": "Tue, 20 Jun 2017 20:00:00 GMT",
            "subject": "테스트",
            "updated": null
        }
    ],
    "meta": {
        "code": 20000,
        "message": "SUCCESS"
    }
}
```
<br><br>


### **생일 등록 API**

#### URI : /api/v1/`calendar/birthday/`

#### Header : `token_required`

#### Http Method : `POST`

#### **Parameters**


**Request**

| Name	| Description | Required | Type |
| --- | --- | --- | --- |
| sdate| birthday | O | "2017-06-19 20:00:00" 형식 / string |

```json
{
  "brithday" : "2017-06-19 20:00:00"

}
```

**Response**

| Name	| Description | Required | Type |
| --- | --- | --- | --- |


```json
// 성공시
{
  "meta": {
    "code": 20000,
    "message": "SUCCESS"
  }
}
```
<br><br>


## 그룹 API

### **그룹 추가 API**

#### URI : /api/v1/`/group/`

#### Header : `token_required`

#### Http Method : `POST`

#### **Parameters**


**Request**

| Name	| Description | Required | Type |
| --- | --- | --- | --- |
| group_name | 그룹 이름 | O | string |

```json
{
  "group_name" : "회식 관련"
}
```

**Response**

| Name	| Description | Required | Type |
| --- | --- | --- | --- |


```json
// 성공시
{
  "meta": {
    "code": 20000,
    "message": "SUCCESS"
  }
}
```
<br><br>


### **일정 수정 API**

#### URI : /api/v1/`group/`

#### Header : `token_required`

#### Http Method : `PUT`

#### **Parameters**


**Request**

| Name	| Description | Required | Type |
| --- | --- | --- | --- |
| group_id | 수정할 그룹 id | O | int |
| group_name | 수정할 그룹 이름 | O | string |


```json
{
  "group_id" : 21,
  "group_name" : "회식 및 저녁 약속 일정"
}
```

**Response**

| Name	| Description | Required | Type |
| --- | --- | --- | --- |


```json
// 성공시
{
  "meta": {
    "code": 20000,
    "message": "SUCCESS"
  }
}
```
<br><br>


### **일정 삭제 API**

#### URI : /api/v1/`group/`

#### Header : `token_required`

#### Http Method : `DELETE`

#### **Parameters**


| Name	| Description | Required | Type |
| --- | --- | --- | --- |
| group_id | 삭제할 그룹 id | O | int |


```json
{
  "group_id" : 21,
}
```

**Response**

| Name	| Description | Required | Type |
| --- | --- | --- | --- |


```json
// 성공시
{
  "meta": {
    "code": 20000,
    "message": "SUCCESS"
  }
}
```
<br><br>


### **그룹 조회 API**

#### URI : /api/v1/`group/`

#### Header : `token_required`

#### Http Method : `GET`

#### **Parameters**


| Name	| Description | Required | Type |
| --- | --- | --- | --- |


**Response**

| Name	| Description | Required | Type |
| --- | --- | --- | --- |


```json
// 성공시
{
    "data": [
        {
            "created": "Mon, 19 Jun 2017 19:22:14 GMT",
            "creator_email": "park@jungi.me",
            "id": 2,
            "name": "테테테스트그룹2",
            "updated": null
        },
        {
            "created": "Mon, 19 Jun 2017 19:23:14 GMT",
            "creator_email": "park@jungi.me",
            "id": 3,
            "name": "하이용",
            "updated": null
        }
    ],
    "meta": {
        "code": 20000,
        "message": "SUCCESS"
    }
}
```
<br><br>


### **전체 그룹(다른 유저가 생성한 그룹도 보임) 조회 API**

#### URI : /api/v1/`group/list/`

#### Header : `token_required`

#### Http Method : `GET`

#### **Parameters**


| Name	| Description | Required | Type |
| --- | --- | --- | --- |


**Response**

| Name	| Description | Required | Type |
| --- | --- | --- | --- |


```json
// 성공시
{
    "data": [
        {
            "created": "Mon, 19 Jun 2017 19:22:14 GMT",
            "creator_email": "park@jungi.me",
            "id": 2,
            "name": "테테테스트그룹2",
            "updated": null
        },
        {
            "created": "Mon, 19 Jun 2017 19:23:14 GMT",
            "creator_email": "park@jungi.me",
            "id": 3,
            "name": "하이용",
            "updated": null
        }
    ],
    "meta": {
        "code": 20000,
        "message": "SUCCESS"
    }
}
```
<br><br>


### **특정 그룹에 일정 추가 API**

#### URI : /api/v1/`group/event/`

#### Header : `token_required`

#### Http Method : `POST`

#### **Parameters**


**Request**

| Name	| Description | Required | Type |
| --- | --- | --- | --- |
| sdate| 일정 시작 일자 | O | "2017-06-19 20:00:00" 형식 / string |
| edate| 일정 종료 일자 | O | "2017-06-19 20:00:00" 형식 / string |
| subject | 일정 제목 | O | string |
| group_id | 일정 등록할 그룹 id | O | int |


```json
{
  "sdate" : "2017-06-19 20:00:00",
  "edate" : "2017-06-19 23:00:00",
  "subject" : "친구들과 약속",
  "group_id" : 13
}
```


**Response**

| Name	| Description | Required | Type |
| --- | --- | --- | --- |


```json
// 성공시
{
  "meta": {
    "code": 20000,
    "message": "SUCCESS"
  }
}
```
<br><br>
