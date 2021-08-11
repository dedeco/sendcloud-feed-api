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

