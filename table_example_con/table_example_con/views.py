from django.shortcuts import render
from django.db import models
from django.http import HttpResponse
import django_tables2 as tables
import MySQLdb
import datetime
import pytz
from django_tables2.config import RequestConfig
import itertools
from django.db import connection
from djqscsv import render_to_csv_response

##### Modify with your database here #####
db = MySQLdb.connect("localhost", "root", "intel@123", "ithome_news", charset='utf8')
cursor = db.cursor()

category_list = ['All', 'iPhone应用推荐', 'iPhone新闻', 'Win10快讯', 'Win10设备', '业界', '人工智能', '人物', '天文航天', '奇趣电子', '安卓应用推荐',
                 '安卓手机', '安卓新闻', '影像器材', '新能源汽车', '智能家居', '智能家电', '活动互动', '游戏快报', '电商', '电子竞技', '电脑硬件', '科技前沿', '科普常识',
                 '笔记本', '网络', '苹果', '车联网', '软件快报', '辣品广告', '通信']


class news(models.Model):
    time = models.CharField(max_length=10, blank=True, null=True)
    title = models.CharField(max_length=10, blank=True, null=True)
    category = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = "news"


class newsTable(tables.Table):
    counter = tables.Column(verbose_name="No", empty_values=(), orderable=False)
    time = tables.Column(verbose_name="Time")
    title = tables.Column(verbose_name="Title")
    category = tables.Column(verbose_name="Category")

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter', itertools.count(1))
        return next(self.row_counter)

    class Meta:
        model = news
        attrs = {
            "class": "info-table",
        }
        fields = ("counter", "time", "title", "category")


def to_render(html_render, data, table):
    html_render['table'] = table
    html_render['category_list'] = category_list


def table_show(request):
    data = news.objects.all()
    data = data.values('time', 'title', 'category')

    table = newsTable(data)  # , row_attrs={'id': lambda record: record['sn']}, order_by="-updated_time")
    RequestConfig(request, paginate={'per_page': 100}).configure(table)

    html_render = {}
    to_render(html_render, data, table)
    return render(request, "index.html", html_render)


# rendering "Search by Title"
def news_search(request):
    data = news.objects.all()
    html_render = {}

    data = data.filter(models.Q(title__icontains=request.GET['keywd_input']))
    data = data.values("time", "title", "category")
    table = newsTable(data)  # , order_by="-time")
    RequestConfig(request, paginate={'per_page': 100}).configure(table)
    to_render(html_render, data, table)
    html_render['keywd_input'] = request.GET['keywd_input']

    return render(request, "index.html", html_render)


# rendering "Filter"
def news_filter(request):
    data = news.objects.all()
    html_render = {}

    if request.GET['filter_category'] == 'All':
        pass
    else:
        data = data.filter(models.Q(category__icontains=request.GET['filter_category']))

    data = data.values("time", "title", "category")
    table = newsTable(data)
    RequestConfig(request, paginate={'per_page': 100}).configure(table)
    to_render(html_render, data, table)
    html_render['filter_category'] = request.GET['filter_category']

    return render(request, "index.html", html_render)


def download_excel(requst):
    data = news.objects.all()
    print(type(data))
    data = data.values("time", "title", "category")
    print(type(data))
    return render_to_csv_response(data, filename="table_download.csv")
