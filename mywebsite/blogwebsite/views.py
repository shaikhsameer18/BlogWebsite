from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from blogwebsite.models import Category, Post

POSTS_PER_PAGE = 9


def home(request):
    cats = Category.objects.all()
    all_posts = Post.objects.all().order_by('-post_id')
    paginator = Paginator(all_posts, POSTS_PER_PAGE)
    posts = paginator.get_page(request.GET.get('page'))
    console_lines = [
        'git log --oneline -1 {}/'.format(p.cat.url) + '  # "{}"'.format(p.title)
        for p in all_posts[:5]
    ] or ['tail -f debuggers.log  # no posts published yet']
    data = {
        'posts': posts,
        'cats': cats,
        'featured': posts[0] if posts else None,
        'console_lines': console_lines,
    }
    return render(request, 'home.html', data)


def about(request):
    return render(request, 'about.html', {'cats': Category.objects.all()})


def post(request, url):
    post_obj = get_object_or_404(Post, url=url)
    cats = Category.objects.all()
    related = Post.objects.filter(cat=post_obj.cat).exclude(pk=post_obj.pk)[:4]
    return render(request, 'posts.html', {
        'post': post_obj,
        'cats': cats,
        'related': related,
        'gutter_lines': range(1, 45),
    })


def category(request, url):
    cat = get_object_or_404(Category, url=url)
    paginator = Paginator(Post.objects.filter(cat=cat).order_by('-post_id'), POSTS_PER_PAGE)
    posts = paginator.get_page(request.GET.get('page'))
    return render(request, 'category.html', {'cat': cat, 'posts': posts, 'cats': Category.objects.all()})
