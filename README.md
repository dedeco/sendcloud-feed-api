# How to run this project

### Build the images and run the containers:

```
docker-compose up -d --build
```

### Test out the following routes:

* [Docs OpenAPI](http://127.0.0.1:8000/docs)

### Components running on docker:
- mongodb: database 
- scheduler: celery
- worker: celery
- rabbitmq: broker celery
- api: using fastapi
- redis: backend celery 

### Commments
In the instructions was predict exercise will take about 8 hours and I was very busy these days. So, I just started a few days ago (13ht) and have just a few hours by day. I apologize for that, but, I could not finish all tests and documentation that I would like to. Tomorrow will turn 14 days, so I prefer to send it because the deadline will expire soon.  I did not create a user model too, but is realy easy to adapt all endpoints to be related a some user and by access by token.

In general, was very fun doing everything. I hope you like it! 

