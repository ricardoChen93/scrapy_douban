#!/usr/bin env python
# -*- coding: utf-8 -*-

from flask import Flask, request, render_template
from pymongo import MongoClient

app = Flask(__name__)
app.debug = True

# Database setting
client = MongoClient()
db = client['douban_movie']
col = db['detail']


@app.route('/', methods=['GET', 'POST'])
def index():
    cpage = int(request.form.get("cpage", 1))
    psize = int(request.form.get("psize", 20))
    country = request.form.get('country', u'中国大陆')
    rating = float(request.form.get('rating', 1.0))
    q = {'country': country, 'rating': {'$gte': rating}}
    movies = col.find(q).sort("rating", -1)
    count = movies.count()
    page = Page(cpage, psize, count)
    movies = movies[page.start:page.end]
    return render_template(
        'index.html', page=page, movies=movies)


class Page():

    def __init__(self, cpage, psize, count):
        self.cpage = cpage
        self.psize = psize
        self.count = count
        self.max_page = (count + psize - 1) / psize
        self.max_page = max(self.max_page, 1)
        self.cpage = min(self.cpage, self.max_page)

        self.start = (self.cpage - 1) * psize
        self.start = 0 if self.start < 0 else self.start
        self.end = self.cpage * psize
        self.end = count if self.end > count else self.end

        # 初始化页码
        self.init_page_num(self.cpage, self.max_page)

    def init_page_num(self, cpage, max_page):
        pass


if __name__ == '__main__':
    app.run()