# scrapy_douban

## Introduction
A distributed web crawler based on scrapy and scrapy_redis.

## Functions
Crawl movies in [douban](https://movie.douban.com/)
and save them in MongoDB.  
Filter movies with Flask app.

## Requirements
* Python2.7
* [Scrapy](https://github.com/scrapy/scrapy) >= 1.2
* [Redis](http://redis.io/) >= 2.8
* [redis-py](https://github.com/andymccurdy/redis-py) >= 2.10
* [scrapy-redis](https://github.com/rolando/scrapy-redis) >= 0.6.3
* [MongoDB](https://www.mongodb.com/) >= 3.2.10
* [pymongo](https://api.mongodb.com/python/3.3.1/) >= 3.3.1
* [flask](https://github.com/pallets/flask) >= 0.10.1

## Usage
1. Clone the repo: `git clone https://github.com/ricardoChen93/scrapy_douban`
2. Edit settings.py: change REDIS related parameters according to the master server.
3. Start crawler and process data
 * Master server  
   Process data: `python process_movie_items.py movie:items`
 * Slave server  
   Start one or more scrapy crawlers: `scrapy crawl movie`
4. Run the flask app: `python app.py`  
goto: http://localhost:5000