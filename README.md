## API instructions
User registration:
```
$ curl -X POST http://127.0.0.1:8000/auth/users/ --data 'username=testuser&password=testpassword'
{"email": "", "username": "testuser", "id":1}
```
User jwt creation:
```
$ curl -X POST http://127.0.0.1:8000/auth/jwt/create/ --data 'username=testuser&password=testpassword'
{"refresh":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIU...","access":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."}
```
Post creation:
```
$ curl -X POST http://127.0.0.1:8000/api/v1/posts/create/ -H 'Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...' --data 'text=abracadabra'
{"text":"abracadabra"}
```
Post like:
```
$ curl -X POST http://127.0.0.1:8000/api/v1/posts/like/ -H 'Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...' --data 'id=1' 
{"status":"success"}
```
Post unlike:
Repeat the previous step

Analytics about how many likes was made:
```
$ curl -X GET -G http://127.0.0.1:8000/api/v1/analytics/ -d date_from=2021-04-02 -d date_to=2021-05-05
[{"id":2,"created_at":"2021-04-04T19:25:24.099292Z","post":1,"liked_by":1},{"id":3,"created_at":"2021-04-04T19:26:11.603805Z","post":1,"liked_by":2},{"total":2}]
```
User activity:
```
$ curl -X GET http://127.0.0.1:8000/api/v1/users/1/ -H 'Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
[{"id":1,"last_login":"2021-04-04T19:24:59.250937Z","last_request":{"date":"2021-04-04T19:25:24.089476Z"}}]
```
