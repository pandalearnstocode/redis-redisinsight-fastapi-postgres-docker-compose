### __Running things in Local:__

```bash
sudo docker-compose build
docker-compose up -d
docker ps
docker-compose down
```

* [Swagger UI](http://localhost:8008/docs)
* [Redis Insight](http://localhost:8001)

![](https://github.com/pandalearnstocode/redis-redisinsight-fastapi-postgres-docker-compose/redis_cache_mini.gif)

### __reference:__

#### __General:__

* https://testdriven.io/blog/fastapi-sqlmodel/
* https://stackoverflow.com/questions/65122957/resolving-new-pip-backtracking-runtime-issue
* https://testdriven.io/blog/fastapi-docker-traefik/
* https://stackoverflow.com/questions/64379089/fastapi-how-to-read-body-as-any-valid-json

#### __Specific:__

* https://collabnix.com/running-redisinsight-using-docker-compose/
* https://rednafi.github.io/digressions/python/database/2020/05/25/python-redis-cache.html
* https://stackoverflow.com/questions/71085983/modern-apis-with-fastapi-redis-caching
* https://stackoverflow.com/questions/15859156/python-how-to-convert-a-valid-uuid-from-string-to-uuid