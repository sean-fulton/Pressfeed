from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Article, Source, Comment, Like, Dislike
from django.core.paginator import Paginator, EmptyPage
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
                if request.POST.get(source.name) == 'on':
                    source.subscribers.add(request.user)

            elif request.POST.get(source.name) == None:
                    source.subscribers.remove(request.user)

        messages.success(request, "You have updated your subscriptions!")
        return redirect(reverse_lazy('subscribe'))

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
    articles_list = Article.objects.filter(source__in=sources).order_by('-published_at')

    paginator = Paginator(articles_list, 8)

    page = request.GET.get('page')
    articles = paginator.get_page(page)

    for article in articles:
        article.has_liked = article.likes.filter(user=user).exists()
        article.has_disliked = article.dislikes.filter(user=user).exists()
    
    return render(request, 'newsfeed.html', {'articles': articles})

@login_required
def article_view(request, pk):
     user = request.user
     article = Article.objects.get(id=pk)
     comments = Comment.objects.filter(article=article)
     comment_form = CommentForm(request.POST or None)
     article.has_liked = article.likes.filter(user=user).exists()
     article.has_disliked = article.dislikes.filter(user=user).exists()

     if request.method == 'POST':
          if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()
            comment_form = CommentForm()
            return redirect(reverse_lazy('article-view', args=[pk]))

     context = {
          'article': article,
          'comments': comments,
          'comment_form': comment_form,
     }

     return render(request, 'article.html', context)

@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    
    if comment.user == request.user:
        if request.method == 'POST':
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
                return redirect(reverse_lazy('article-view', args=[comment.article.id]))
        else:
            form = CommentForm(instance=comment)
        return redirect(reverse_lazy('edit-comment', args=[pk]))
    else:
        return redirect(reverse_lazy('article-view', args=[comment.article.id]))


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)

    if comment.user == request.user:
        if request.method == 'POST':
            comment.delete()
            return redirect(reverse_lazy('article-view', args=[comment.article.id]))
        return redirect(reverse_lazy('delete-comment', args=[pk]))
    else:
        return redirect(reverse_lazy('article-view', args=[comment.article.id]))

@login_required
def like_article(request, pk, view):
    article = get_object_or_404(Article, pk=pk)
    user = request.user
    like = Like.objects.filter(user=user, article=article).first()

    if like:
        like.delete()
    else:
        like = Like(user=user, article=article)
        like.save()

        dislike = Dislike.objects.filter(user=user, article=article).first()
        if dislike:
            dislike.delete()

    if (view == 'article-view'):
        return redirect(reverse_lazy(view, args=[pk]))
    else:
        return redirect(reverse_lazy(view))


def dislike_article(request, pk, view):
    article = get_object_or_404(Article, pk=pk)
    user = request.user
    dislike = Dislike.objects.filter(user=user, article=article).first()

    if dislike:
        dislike.delete()
    else:
        dislike = Dislike(user=user, article=article)
        dislike.save()

        like = Like.objects.filter(user=user, article=article).first()
        if like:
            like.delete()
      
    if (view == 'article-view'):
        return redirect(reverse_lazy(view, args=[pk]))
    else:
        return redirect(reverse_lazy(view))

    
