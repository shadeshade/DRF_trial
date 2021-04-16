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
$ curl -X POST http://127.0.0.1:8000/api/v1/posts/ -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...' --data 'text=abracadabra'
{"id":1}
```
Post like:      
```
$ curl -X POST http://127.0.0.1:8000/api/v1/posts/1/like/ -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
{}
```
Post unlike:
```
$ curl -X POST http://127.0.0.1:8000/api/v1/posts/1/unlike/ -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
{}
```
Posts list:
```
$ curl -X GET http://127.0.0.1:8000/api/v1/posts/ -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
[
    {
        "id": 1,
        "author_id": 1,
        "text": "new post text",
        "likes_count": 3,
        "date_posted": "2021-04-04T19:24:38.034098Z"
    },
     {
        "id": 3,
        "author_id": 3,
        "text": "abracadaabra",
        "likes_count": 0,
        "date_posted": "2021-04-05T09:57:41.562929Z"
    }
]
```
Analytics about how many likes were made:
```
$ curl -X GET -G http://127.0.0.1:8000/api/v1/analytics/ -d date_from=2021-04-13 -d date_to=2021-05-16 -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "day": "2021-04-14T00:00:00Z",
            "likes_count": 2
        },
        {
            "day": "2021-04-15T00:00:00Z",
            "likes_count": 1
        }
    ],
    "total_likes": 3
}
```
User activity list:
```
$ curl -X GET http://127.0.0.1:8000/api/v1/users/ -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
[
    {
        "id": 1,
        "last_login": "2021-04-05T16:12:12.350723Z",
        "last_request": "2021-04-04T19:25:24.089476Z"
    },
    {
        "id": 2,
        "last_login": "2021-04-05T15:56:51.384347Z",
        "last_request": "2021-04-04T19:26:11.592291Z"
    }
]
```
User activity:
```
$ curl -X GET http://127.0.0.1:8000/api/v1/users/1/ -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
[{ "last_login": "2021-04-05T16:12:12.350723Z", "last_request": "2021-04-04T19:25:24.089476Z"}]
```
