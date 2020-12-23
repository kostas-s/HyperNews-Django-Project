from collections import OrderedDict

from django.shortcuts import render
from django.views import View
import json
from django.conf import settings
from datetime import datetime
from django.http import HttpResponse, Http404
import collections
from news import models
from django.shortcuts import redirect


class GetNewsView(View):

    def get(self, request, link):
        #with open(settings.NEWS_JSON_PATH, 'r') as json_read:
            #news_content = json.load(json_read)
        news_content = models.load_news()
        if int(link) > len(news_content) or int(link) == 0:
            raise Http404
        context = news_content[int(link) - 1]
        return render(request, f"news/viewnews.html", context={
            'created': context.get("created"),
            'text': context.get("text"),
            'title': context.get("title"),
            'link': context.get("link")
        })

class IndexView(View):
    def get(self, request, *args, **kwargs):
        #return HttpResponse("<html><p>Coming soon</p></html>")
        return redirect('/news/')

class NewsListView(View):
    def get(self, request, *args, **kwargs):
        news_content = models.get_news_sorted(request.GET.get('q'))
        return render(request, f"news/index.html", {"context": dict(news_content)})

class CreateNewsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, f"news/createnews.html")

    def post(self, request, *args, **kwargs):
        news_content = models.load_news()
        date = datetime.now()
        new_entry = {'created': str(date.strftime("%Y-%m-%d %H:%M:%S")),
                     'title': request.POST.get('title'),
                     'text': request.POST.get('text'),
                     'link':str(len(news_content)+1)}
        models.add_news(new_entry)
        return redirect('/news/')