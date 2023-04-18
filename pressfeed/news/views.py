from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Article, Source, Comment
from pressfeed.forms import CommentForm
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
import environ

env = environ.Env()
environ.Env.read_env()

@login_required
def subscribe(request):
    sources = Source.objects.all()

    # If form submitted and valid, process subscription/unsubscription
    if request.method == 'POST':
        for source in sources:
            if source.name in request.POST:
                # If source is checked and user is not subscribed, subscribe user
                print(request.POST.get(source.name))
                if request.POST.get(source.name) == 'on':
                    source.subscribers.add(request.user)
                # If source is unchecked and user is subscribed, unsubscribe user
            elif request.POST.get(source.name) == None:
                    source.subscribers.remove(request.user)

        messages.success(request, "You have updated your subscriptions!")
        return redirect('subscribe')

    # If no form submitted, show user's subscribed sources
    user_sources = request.user.sources.all()
    return render(request, 'subscribe.html', {'sources': sources, 'user_sources': user_sources})

def testfeed(request):
    # use NewsAPI call to fetch article data
    # start = time.time()
    # irish_news_request = requests.get(f'https://newsapi.org/v2/top-headlines?country=ie&apiKey={env("NEWSAPI_KEY")}')
    # newsapi_response = json.loads(irish_news_request.content)
    # end = time.time()
    # print(f'TIME TO CALL API: {end - start}')
    # return render(request, 'testfeed.html', {'api': newsapi_response})

    # use PostgreSQL Article model to fetch article data

    articles = Article.objects.order_by('-published_at')
    return render(request, 'testfeed.html', {'articles': articles})

@login_required
def newsfeed(request):
    user = request.user
    sources = user.sources.all()
    articles = Article.objects.filter(source__in=sources).order_by('-published_at')
    return render(request, 'newsfeed.html', {'articles': articles})

@login_required
def article_view(request, pk):
     article = Article.objects.get(id=pk)
     comments = Comment.objects.filter(article=article)
     form = CommentForm(request.POST or None)

     if request.method == 'POST':
          if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()
            form = CommentForm()

     context = {
          'article': article,
          'comments': comments,
          'form': form,
     }

     return render(request, 'article.html', context)

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)

    if comment.user == request.user:
        comment.delete()
    return redirect(reverse_lazy('article-view', args=[comment.article.id]))


    
