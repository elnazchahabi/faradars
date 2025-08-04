from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Post, Category, Tag
from .forms import CommentForm, NewsletterForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest


User = get_user_model()

def post_list(request, category_slug=None, tag_slug=None, year=None, month=None):
    posts = Post.objects.filter(status='published', published_date__lte=timezone.now())
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)
    if year and month:
        posts = posts.filter(published_date__year=year, published_date__month=month)
    q = request.GET.get('q')
    if q:
        posts = posts.filter(Q(title__icontains=q) | Q(content__icontains=q))
    level = request.GET.get('level')
    if level:
        posts = posts.filter(level=level)

    paginator = Paginator(posts, 5)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj':       page_obj,
        'LEVEL_CHOICES':  Post.LEVEL_CHOICES,
        'archive_dates':  Post.objects.dates('published_date','month',order='DESC'),
        'categories':     Category.objects.all(),
        'tags':           Tag.objects.all(),
        'form':           CommentForm(),
        'newsletter_form': NewsletterForm(),
    }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published', published_date__lte=timezone.now())
    comments = post.comments.filter(approved=True, parent__isnull=True)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user if request.user.is_authenticated else None
            comment.save()
            return redirect(post.get_absolute_url())
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {
        'post':           post,
        'comments':       comments,
        'form':           form,
        'newsletter_form': NewsletterForm(),
    })




@login_required
def like_post(request, slug):
    if request.method != 'POST':
        return HttpResponseBadRequest()
    post = get_object_or_404(Post, slug=slug)
    user = request.user

    # اگر قبلاً دیس‌لایک زده، اول حذفش کن
    if post.disliked_by.filter(pk=user.pk).exists():
        post.disliked_by.remove(user)
    # اگر قبلاً لایک نزده، اضافه کن؛ در غیر این صورت لایک را بردار (toggle)
    if post.liked_by.filter(pk=user.pk).exists():
        post.liked_by.remove(user)
    else:
        post.liked_by.add(user)

    return JsonResponse({'likes': post.likes, 'dislikes': post.dislikes})


@login_required
def dislike_post(request, slug):
    if request.method != 'POST':
        return HttpResponseBadRequest()
    post = get_object_or_404(Post, slug=slug)
    user = request.user

    if post.liked_by.filter(pk=user.pk).exists():
        post.liked_by.remove(user)
    if post.disliked_by.filter(pk=user.pk).exists():
        post.disliked_by.remove(user)
    else:
        post.disliked_by.add(user)

    return JsonResponse({'likes': post.likes, 'dislikes': post.dislikes})


def newsletter_subscribe(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect(request.META.get('HTTP_REFERER','/'))


def author_panel(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'blog/author_panel.html', {'posts': posts})


def author_profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=author, status='published')
    return render(request, 'blog/author_profile.html', {'author': author, 'posts': posts})





from django.views.generic import DetailView
from django.contrib.auth import get_user_model
from .models import Post

User = get_user_model()

class AuthorProfileView(DetailView):
    model = User
    template_name = 'blog/author_profile.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # بیوگرافی از فیلد profile (اگر جدا داری) یا از user.bio
        ctx['bio'] = getattr(self.object, 'profile', None) and self.object.profile.bio or ''
        # پست‌های این نویسنده
        ctx['posts'] = Post.objects.filter(author=self.object).order_by('-published_date')
        return ctx
